from django.shortcuts import render
from django.http import HttpResponse, Http404
# Create your views here.
import json
from datetime import datetime, date, timedelta
import random

from .models import Student, Lab, LabsScheam, LabDesk, TimeSlot, Records
from .models import Parameter
from .serializers import StudentSerializer, LabSerializer, LabsScheamSerializer
from .serializers import LabDeskSerializer, TimeSlotSerializer
from .serializers import RecordsSerializer

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


def labinfos(request):
    rs = {"number": 3, "info": [{"id": "140556", "name": "amplifier"}, {
        "id": "556413", "name": "filter"},
        {"id": "220321", "name": "power amplifier"}]}
    return HttpResponse(json.dumps(rs), content_type='application/json')


def timeSelect(request):
    startTime = datetime.strptime('2016-06-10-08-00', '%Y-%m-%d-%H-%M')
    slotTime = timedelta(minutes=60)
    breakTime = timedelta(minutes=5)
    timegroup = [[(startTime + slotTime * i).strftime('%Y-%m-%d-%H-%M'),
                  (startTime + slotTime * i - breakTime).strftime('%Y-%m-%d-%H-%M')]
                 for i in range(13)]
    resources = [str(random.randint(1, 10)) + '/10' for i in range(13)]
    rs = {"id": "140556", "name": "amplifier",
          "timegroup": timegroup, "remain": resources}
    return HttpResponse(json.dumps(rs), content_type='application/json')


class StudentViewSet(viewsets.ReadOnlyModelViewSet):

    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class LabViewSet(viewsets.ModelViewSet):

    """
    """
    queryset = Lab.objects.all()
    serializer_class = LabSerializer


class LabsScheamViewSet(viewsets.ModelViewSet):

    """
    """
    queryset = LabsScheam.objects.all()
    serializer_class = LabsScheamSerializer


# class LabDeskViewSet(viewsets.ModelViewSet):

    #     """
    #     """
    #     queryset = LabDesk.objects.all()
    #     serializer_class = LabDeskSerializer


class TimeSlotViewSet(viewsets.ModelViewSet):

    """
    """
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer


class RecordsViewSet(viewsets.ModelViewSet):

    """
    """
    queryset = Records.objects.all()
    serializer_class = RecordsSerializer


class LabDeskList(generics.ListCreateAPIView):
    queryset = LabDesk.objects.all()
    serializer_class = LabDeskSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('deskID',)


class LabDeskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LabDesk.objects.all()
    serializer_class = LabDeskSerializer


class StudentUnorderLabList(generics.ListAPIView):

    serializer_class = LabSerializer

    def get_queryset(self):
        try:
            paras = Parameter.objects.get(pk=1)
            student = Student.objects.get(studentID=self.kwargs['studentID'])
        except Parameter.DoesNotExist, Student.DoesNotExist:
            raise Http404
        today = date.today()
        deltaDay = timedelta(days=paras.preDay)
        candidateLabs = student.labscheam.labs.filter(
            startDate__lte=(today + deltaDay), endDate__gte=(today + deltaDay))
        finishLabs = student.finishLabs.all()
        return [lab for lab in candidateLabs if lab not in finishLabs]


@api_view()
def LabResourcesList(request, studentID, labID):
    """
    remain resources of a specific Lab
    """
    try:
        paras = Parameter.objects.get(pk=1)
        lab = Lab.objects.get(pk=labID)
    except Parameter.DoesNotExist, Lab.DoesNotExist:
        raise Http404
    deltaDay = timedelta(days=paras.preDay)
    today = date.today()
    if not lab.startDate or lab.startDate > today + deltaDay or lab.endDate < today + deltaDay:
        return Response({'message': 'lab error'},
                        status=status.HTTP_404_NOT_FOUND)
    labTypeID = lab.labCategory.pk
    totalNum = len(LabDesk.objects.filter(labCategory__pk=labTypeID))
    rs = []
    while not today == lab.endDate:
        today = today + deltaDay
        for duration in TimeSlot.objects.all():
            content = {"date": today, "time": "",
                       "totalNum": totalNum, "occupyNum": "", "isU": False}
            occResources = Records.objects.filter(
                date=today, timeSlot=duration)
            if occResources.filter(student__studentID=studentID):
                content["isU"] = True
            content["time"] = TimeSlotSerializer(duration).data
            content["occupyNum"] = len(occResources)
            rs.append(content)
    return Response(rs, status.HTTP_200_OK)
