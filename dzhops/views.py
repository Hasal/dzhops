# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index(request):
    return render_to_response('index.html')

def login(request):
    ret = '1243'
    status = 'False'
    return render_to_response('login.html',{'ret': ret, 'status': status })
