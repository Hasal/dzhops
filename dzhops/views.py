# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index(request):
    return render_to_response('index.html')

def login(request):
    ret = {'zhaogb-201':{'cont':'zhaogb-201','status': 'True'},'zhaogb-202':{'cont':'zhaogb-202','status': 'Fasle'},'zhaogb-203':{'cont':'zhaogb-203','status': 'Fasle'},'zhaogb-205':{'cont':'zhaogb-205','status': 'True'}}

    return render_to_response('login.html',{'ret': ret})
