from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import redirect, render
from apps.authentication.models import *


@login_required(login_url="/login/")
def index(request):
    context = {
        'segment': 'dashboard'
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def users_view(request):
    my_queryset = MegaUser.objects.filter(is_superuser=False).all()
    search_query = request.GET.get('q')
    if search_query:
        my_queryset = my_queryset.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) |
                                         Q(phone__icontains=search_query) | Q(card_code__icontains=search_query)
                                         | Q(card_name__icontains=search_query))
    paginator = Paginator(my_queryset, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'segment': 'users'
    }
    return render(request, 'home/users.html', context)


