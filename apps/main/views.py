from django.shortcuts import render
from rest_framework import generics, status
from .serializers import *
from rest_framework import permissions


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ManufacturerView(generics.ListAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class SaleView(generics.ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class UserSaleView(generics.ListAPIView):
    queryset = UserSale.objects.all()
    serializer_class = UserSaleSerializer
    permission_classes = [permissions.IsAuthenticated]





