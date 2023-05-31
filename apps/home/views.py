from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from apps.authentication.models import *
from apps.main.forms import *


@login_required(login_url="/login/")
def index(request):
    cashback = Cashback.objects.all()
    context = {
        'segment': 'dashboard',
        'cashbacks': cashback
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def users_view(request):
    my_queryset = MegaUser.objects.filter(is_superuser=False).all().order_by('id')
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


def categories(request):
    categories = Category.objects.all().order_by('id')
    search_query = request.GET.get('q')
    if search_query:
        categories = categories.filter(Q(groupname__icontains=search_query) | Q(number__icontains=search_query))
    paginator = Paginator(categories, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        "segment": "cats"
    }
    html_template = loader.get_template('home/categories.html')
    return HttpResponse(html_template.render(context, request))


def category_detail(request, pk):
    category = Category.objects.get(id=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('home_categories')
    else:
        form = CategoryForm(instance=category)

    return render(request,
                  'home/category_detail.html',
                  {'form': form, 'category': category, 'segment': 'cats'})


def sub_categories(request):
    categories = SubCategory.objects.all().order_by('id')
    search_query = request.GET.get('q')
    if search_query:
        categories = categories.filter(Q(name__icontains=search_query) | Q(code__icontains=search_query))
    paginator = Paginator(categories, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        "segment": "subcategories"
    }
    html_template = loader.get_template('home/subcategories.html')
    return HttpResponse(html_template.render(context, request))


def subcategory_detail(request, pk):
    subcategory = SubCategory.objects.get(id=pk)

    if request.method == 'POST':
        form = SubCategoryForm(request.POST, request.FILES, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('home_subcategories')
    else:
        form = SubCategoryForm(instance=subcategory)

    return render(request,
                  'home/subcategory_detail.html',
                  {'form': form, 'subcategory': subcategory, 'segment': 'subcategories'})


def manufacturers(request):
    categories = SubCategory.objects.all().order_by('id')
    search_query = request.GET.get('q')
    if search_query:
        categories = categories.filter(Q(manufacrurer_name__icontains=search_query) | Q(code__icontains=search_query))
    paginator = Paginator(categories, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        "segment": "manufacturer"
    }
    html_template = loader.get_template('home/manufacturers.html')
    return HttpResponse(html_template.render(context, request))


def manufacturer_detail(request, pk):
    manufacturer = Manufacturer.objects.get(id=pk)

    if request.method == 'POST':
        form = ManufacturerForm(request.POST, request.FILES, instance=manufacturer)
        if form.is_valid():
            form.save()
            return redirect('home_manufacturers')
    else:
        form = ManufacturerForm(instance=manufacturer)

    return render(request,
                  'home/manufacturer_detail.html',
                  {'form': form, 'subcategory': manufacturer, 'segment': 'manufacturer'})


def products(request):
    products = Product.objects.all().order_by('id')
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(Q(itemname__icontains=search_query) | Q(itemcode__icontains=search_query))
    paginator = Paginator(products, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        "segment": "product"
    }
    html_template = loader.get_template('home/products.html')
    return HttpResponse(html_template.render(context, request))


def product_detail(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home_products')
        else:
            print("ERROR: ", form.errors)
    else:
        form = ProductForm(instance=product)

    return render(request,
                  'home/product_detail.html',
                  {'form': form, 'product': product, 'segment': 'product'})


def cashback_detail(request, pk):
    cashback = Cashback.objects.get(id=pk)

    if request.method == 'POST':
        form = CashbackForm(request.POST, request.FILES, instance=cashback)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CashbackForm(instance=cashback)

    return render(request,
                  'home/cashback_detail.html',
                  {'form': form, 'cashback': cashback, 'segment': 'product'})

