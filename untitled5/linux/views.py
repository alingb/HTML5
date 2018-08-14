from django.shortcuts import render

# Create your views here.

import json

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from linux.models import Teacher


def index(request):
    teacher1 = Teacher(name='ajing', age=18, sex="man", subject="python运维开发", telphone='18910148469')
    teacher2 = Teacher(name='ling', age=28, sex="women", subject="linux运维", telphone='15312344321')
    teacher3 = Teacher(name='laomo', age=48, sex="man", subject="web开发", telphone='18912344321')
    teacher4 = Teacher(name='laomo', age=48, sex="man", subject="web开发", telphone='18912344321')
    teacher5 = Teacher(name='laomo', age=48, sex="man", subject="web开发", telphone='18912344321')
    teacher6 = Teacher(name='laomo', age=48, sex="man", subject="web开发", telphone='18912344321')
    teacher1.save()
    print("save teacher1")
    teacher2.save()
    print("save teacher2")
    teacher3.save()
    teacher4.save()
    teacher5.save()
    teacher6.save()
    print("save teacher3")
    return HttpResponse("save 3 teachers into mysql.")

def test(request, **kwargs):
    return render(request, 'html/teachlist.html')

def hello(request, arg1, arg2):
    return HttpResponse("<h1 style='text-align:center'>hello {0}, hello {1}</h1>".format(arg1, arg2))

def keyword(request, ip):
    return HttpResponse("<h1 style='text-align:center'>this ip is:  {0}</h1>".format(ip))

def redirect(request):
    return HttpResponseRedirect(reverse("index"))

def teacherList(request):
    teachers = Teacher.objects.all()
    print(teachers)
    data = list()
    for each in teachers:
        eachdata = dict()
        eachdata["name"] = each.name
        eachdata["age"] = each.age
        eachdata["sex"] = each.sex
        eachdata["subject"] = each.subject
        eachdata["telphone"] = each.telphone
        data.append(eachdata)

    resultBean = dict()
    resultBean["code"] = 200
    resultBean["msg"] = 'success'
    resultBean["data"] = data

    return JsonResponse(resultBean)
