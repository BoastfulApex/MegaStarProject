from django.contrib import admin
from .models import *


admin.site.register(Order)
admin.site.register(Sale)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(UserSale)