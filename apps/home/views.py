from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from apps.authentication.forms import *


@login_required(login_url="/login/")
def index(request):
    context = {
        
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))
