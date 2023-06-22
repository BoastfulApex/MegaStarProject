from django.urls import path
from .views import *

urlpatterns = [

    path('categories/', CategoryView.as_view(), name='categories'),
    path('sub_categories/', SubCategoryView.as_view(), name='sub_categories'),
    path('manufacturers/', ManufacturerView.as_view(), name='manufacturers'),
    path('sales/', SaleView.as_view(), name='sales'),
    path('user_lases/', UserSaleView.as_view(), name='user_sales'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('order_details/', OrderDetailView.as_view(), name='order_details'),
    path('products/', ProductView.as_view(), name='products'),

    path('user_totals/', UserTotalStatusView.as_view(), name='user_totals'),
    path('top_products/', TopProductAPIView.as_view(), name='top_products'),
    path('similar_products/', SimilarProductView.as_view(), name='similar_products'),
    path('sale_products/', SaleProducts.as_view(), name='sale_products'),

    path('check_promocode/', CheckPromoCode.as_view(), name='check_promocode'),

    path('qr_code/', QrCodeView.as_view(), name='qr_code'),

    path('cards/', CardView.as_view(), name='cards'),
    path('cards/<int:pk>', CardObject.as_view(), name='card-object'),
    path('add_order', AddOrderView.as_view(), name='add-order'),

    path('users/', UserListView.as_view(), name='api-users'),

]
