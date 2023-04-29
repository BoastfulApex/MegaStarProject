from django.urls import path
from .views import *

urlpatterns = [

    path('categories', CategoryView.as_view(), name='categories'),
    path('sub_categories', SubCategoryView.as_view(), name='sub_categories'),
    path('manufacturers', ManufacturerView.as_view(), name='manufacturers'),
    path('sales', SaleView.as_view(), name='sales'),
    path('user_lases', UserSaleView.as_view(), name='user_sales'),
    path('orders', OrderView.as_view(), name='orders'),
    path('order_details', OrderDetailView.as_view(), name='order_details'),

    path('products', ProductView.as_view(), name='products'),

    path('user_totals', UserTotalStatusView.as_view(), name='user_totals    '),
]