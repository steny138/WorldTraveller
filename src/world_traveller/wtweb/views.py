# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html', {
        'current_time': datetime.now().strftime('%Y-%m-%d(%a) %H:%M:%S'),
    })