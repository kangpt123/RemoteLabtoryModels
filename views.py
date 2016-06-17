from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import json
from datetime import datetime
from datetime import timedelta
import random


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def labinfos(request):
    rs = {"number": 3, "info": [{"id": "140556", "name": "amplifier"}, {
        "id": "556413", "name": "filter"}, {"id": "220321", "name": "power amplifier"}]}
    return HttpResponse(json.dumps(rs), content_type='application/json')


def timeSelect(request):
    startTime = datetime.strptime('2016-06-10-08-00', '%Y-%m-%d-%H-%M')
    slotTime = timedelta(minutes=60)
    breakTime = timedelta(minutes=5)
    timegroup = [[(startTime+slotTime*i).strftime('%Y-%m-%d-%H-%M'), 
    (startTime+slotTime*i-breakTime).strftime('%Y-%m-%d-%H-%M')]
                 for i in range(13)]
    resources = [str(random.randint(1, 10))+'/10' for i in range(13)]
    rs = {"id": "140556", "name": "amplifier",
          "timegroup": timegroup, "remain": resources}
    return HttpResponse(json.dumps(rs), content_type='application/json')
