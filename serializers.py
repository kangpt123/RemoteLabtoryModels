# -*- coding: utf-8 -*-
from rest_framework import serializers
from polls.models import Student, Lab, LabsScheam, LabDesk, TimeSlot
from polls.models import OrderRecords, ActionRecords


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
    deskID = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderRecords
        fields = ('pk', 'deskID', 'timeSlot', 'date', 'student', 'lab')

    def getAvailableDesk(self, data):
        """
        寻找一个未使用的deskID
        """
        occupyRecords = OrderRecords.objects.filter(
            timeSlot=data['timeSlot'], date=data['date'],
            deskID__labCategory=data['lab'].labCategory)
        occupyDesk = map(lambda x: x.deskID, occupyRecords)
        totalDesk = LabDesk.objects.filter(labCategory=data['lab'].labCategory)
        available = set(totalDesk).difference(set(occupyDesk))
        return available

    def validate(self, data):
        """
        """
        if len(self.getAvailableDesk(data)) == 0:
            raise serializers.ValidationError("no desks left")
        return data

    def create(self, data):
        # 存在一个问题，如果用viewSet的话，
        # 这里非得要加一个save动作吗？怎么有时候又好，真是诡异的一笔
        available = self.getAvailableDesk(data)
        data['deskID'] = available.pop()
        rs = super(OrderRecordsSerializer, self).create(data)
        return rs

    def update(self, instance, data):
        available = self.getAvailableDesk(data)
        data['deskID'] = available.pop()
        rs = super(OrderRecordsSerializer, self).update(instance, data)
        return rs


class ActionRecordsSerializer(serializers.ModelSerializer):
    OrderRecordID = serializers.PrimaryKeyRelatedField(read_only=True)
    action = serializers.CharField(required=False)

    class Meta:
        model = ActionRecords
        fields = ('OrderRecordID', 'action')
        # lookup_field = 'OrderRecordID__pk'

    def update(self, instance, data):
        if 'action' not in data.keys() and not instance.action:
            data['action'] = '0'
        elif 'action' not in data.keys():
            data['action'] = '1'
        rs = super(ActionRecordsSerializer, self).update(instance, data)
        return rs
