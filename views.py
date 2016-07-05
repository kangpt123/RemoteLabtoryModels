# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404
# Create your views here.
import json
from itertools import chain
from datetime import datetime, date, timedelta
import random
import django_filters

from .models import Student, Lab, LabsScheam, LabDesk, TimeSlot, OrderRecords
from .models import Parameter, ActionRecords
from .serializers import StudentSerializer, LabSerializer, LabsScheamSerializer
from .serializers import LabDeskSerializer, TimeSlotSerializer
from .serializers import OrderRecordsSerializer, ActionRecordsSerializer

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


class OrderRecordsFilter(filters.FilterSet):

    class Meta:
        model = OrderRecords
        fields = {
            'student': ['exact'],
            'date': ['exact'],
            'timeSlot__startTime': ['lte'],
            'timeSlot__endTime': ['gte']
        }


class OrderRecordsViewSet(viewsets.ModelViewSet):

    """
    """
    queryset = OrderRecords.objects.all()
    serializer_class = OrderRecordsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = OrderRecordsFilter


class LabDeskList(generics.ListCreateAPIView):
    queryset = LabDesk.objects.all()
    serializer_class = LabDeskSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('deskID',)


class LabDeskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LabDesk.objects.all()
    serializer_class = LabDeskSerializer


class queryOrderableLabList(generics.ListAPIView):
    # raise exception 处需要打一个logger

    """
    """
    serializer_class = LabSerializer

    def get_queryset(self):
        try:
            paras = Parameter.objects.get(pk=1)
            student = Student.objects.get(studentID=self.kwargs['studentID'])
        except (Parameter.DoesNotExist, Student.DoesNotExist):
            raise Http404("Parameter.DoesNotExist or Student.DoesNotExist")
        today = date.today()
        deltaDay = timedelta(days=paras.preDay)
        candidateLabs = student.labscheam.labs.filter(
            startDate__lte=(today + deltaDay), endDate__gte=(today + deltaDay))
        return candidateLabs


class hasOrderLab(generics.ListAPIView):
    # 没有限制它的GET, POST方法
    serializer_class = OrderRecordsSerializer

    def get_queryset(self):
        now = datetime.now()
        userRecords = OrderRecords.objects.filter(
            student__studentID=self.kwargs['studentID'], lab__pk=self.kwargs['labID'])
        todayRecords = userRecords.filter(date__gte=now.date())
        nextDayRecords = userRecords.filter(
            date=now.date(), timeSlot__startTime__gte=now.time())
        return list(chain(todayRecords, nextDayRecords))


@api_view()
def labResourceList(request, labID):
    """
    根据orderRecords表中的对应实验桌和时间段的占用情况返回可用资源列表。
    """
    try:
        paras = Parameter.objects.get(pk=1)
        lab = Lab.objects.get(pk=labID)
    except (Parameter.DoesNotExist, Lab.DoesNotExist):
        raise Http404("Parameter or LabID DoesNotExist")
    deltaDay = timedelta(days=paras.preDay)
    today = date.today()
    if not lab.startDate or lab.startDate > today + deltaDay or lab.endDate < today + deltaDay:
        return Response([], status=status.HTTP_200_OK)
    labTypeID = lab.labCategory.pk
    totalNum = len(LabDesk.objects.filter(labCategory__pk=labTypeID))
    rs = []
    while not today == lab.endDate:
        today = today + deltaDay
        for duration in TimeSlot.objects.all():
            content = {"date": today, "time": "",
                       "totalNum": totalNum, "occupyNum": "", "isU": False}
            occResources = OrderRecords.objects.filter(
                date=today, timeSlot=duration)
            content["time"] = TimeSlotSerializer(duration).data
            content["occupyNum"] = len(occResources)
            rs.append(content)
    return Response(rs, status.HTTP_200_OK)


class ActionRecordsViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = ActionRecordsSerializer
    queryset = ActionRecords.objects.all()
    lookup_field = 'OrderRecordID__pk'

    def get_object(self):
        if self.request.method == 'PUT':
            orderRec = OrderRecords.objects.get(
                pk=self.kwargs['OrderRecordID__pk'])
            obj, created = ActionRecords.objects.get_or_create(
                OrderRecordID=orderRec)
            return obj
        else:
            return super(ActionRecordsViewSet, self).get_object()

# def update(self, request, *args, **kwargs):
#     pass
