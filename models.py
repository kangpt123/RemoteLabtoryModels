# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.


class TimeSlot(models.Model):
    startTime = models.TimeField()
    endTime = models.TimeField()
# need to add verification that promise endTime is larger than startTime

    def __str__(self):
        return 'from ' + str(self.startTime) + ' to ' + str(self.endTime)

    class Meta:
        ordering = ["startTime"]


class Instrument(models.Model):
    INSTRUMENT_NAME = (
        ('osc', u'示波器'), ('gen', u'函数信号发生器'), ('met', u'万用表'), ('pow', u'电源'))
    ID = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=3, choices=INSTRUMENT_NAME)
    Position = models.ForeignKey(
        'LabDesk', on_delete=models.SET_NULL, blank=True, null=True)
# 添加一个所属实验桌的属性好不好，待斟酌

    def __str__(self):
        return self.ID


class LabCategory(models.Model):
    categoryName = models.CharField(max_length=20)

    def __str__(self):
        return self.categoryName


class Lab(models.Model):
    labName = models.CharField(max_length=50)
    labCategory = models.ForeignKey(
        LabCategory, on_delete=models.SET_NULL, blank=True, null=True)
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)
# 需要添加什么开放时间这些属性吗

    def __str__(self):
        return self.labName


class Parameter(models.Model):
    preDay = models.IntegerField()
    mostDay = models.IntegerField()


class LabDesk(models.Model):
    deskID = models.IntegerField()
    labCategory = models.ForeignKey(
        LabCategory, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.labCategory.categoryName + " Desk:" + str(self.deskID)


class Records(models.Model):
    deskID = models.ForeignKey(LabDesk, on_delete=models.CASCADE)
    timeSlot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    date = models.DateField()
    student = models.ForeignKey(
        'Student', on_delete=models.SET_NULL, blank=True, null=True)
    orderTime = models.DateTimeField(auto_now_add=True)


class Student(models.Model):
    studentID = models.CharField(primary_key=True, max_length=9)
    name = models.CharField(max_length=20)
    token = models.CharField(max_length=100, blank=True, null=True)
    labscheam = models.ForeignKey(
        'LabsScheam', on_delete=models.CASCADE, blank=True, null=True)
    finishLabs = models.ManyToManyField(Lab, blank=True)
# 需要添加什么待完成实验或者待预定实验

    def __str__(self):
        return self.studentID + ' : ' + self.name


class LabsScheam(models.Model):
    labs = models.ManyToManyField(Lab)
    scheamName = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.scheamName
