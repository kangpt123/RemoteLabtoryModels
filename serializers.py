from rest_framework import serializers
from polls.models import Student, Lab, LabsScheam, LabDesk, TimeSlot
from polls.models import OrderRecords


class LabSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lab
        fields = ('url', 'labName', 'labCategory', 'startDate', 'endDate')


class LabsScheamSerializer(serializers.ModelSerializer):

    labs = LabSerializer(many=True)

    class Meta:
        model = LabsScheam
        fields = ('labs', 'scheamName')


class StudentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Student
        fields = ('url', 'studentID', 'name', 'labscheam')


class LabDeskSerializer(serializers.ModelSerializer):

    class Meta:
        model = LabDesk
        fields = ('url', 'deskID', 'labCategory')


class TimeSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeSlot
        fields = ('startTime', 'endTime')


class OrderRecordsSerializer(serializers.ModelSerializer):

    # timeSlot = TimeSlotSerializer()

    class Meta:
        model = OrderRecords
        fields = ('deskID', 'timeSlot', 'date', 'student', 'orderTime', 'lab')
