from django.urls import path
from apps.home import views

urlpatterns = [

    path('', views.index, name='home'),
    path('users/', views.users_view, name='users'),
    path('categories/', views.categories, name='home_categories'),
    path('categories/<int:pk>', views.category_detail, name='category_update'),
    path('subcategories/', views.sub_categories, name='home_subcategories'),
    path('subcategories/<int:pk>', views.subcategory_detail, name='subcategory_update'),
    path('manufacturers/', views.manufacturers, name='home_manufacturers'),
    path('manufacturers/<int:pk>', views.manufacturer_detail, name='manufacturer_update'),
    path('cashback/<int:pk>', views.cashback_detail, name='cashback_update'),
    path('products/', views.products, name='home_products'),
    path('products/<int:pk>', views.product_detail, name='product_update'),
    path('cashbacks_by_cashback/<int:pk>', views.user_cashback_by_cashback, name='cashbacks_by_cashback'),

]
