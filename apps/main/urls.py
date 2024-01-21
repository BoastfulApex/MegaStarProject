from django.urls import path
from .views import *

urlpatterns = [

    path('categories/', CategoryView.as_view(), name='categories'),
    path('sub_categories/', SubCategoryView.as_view(), name='sub_categories'),
    path('manufacturers/', ManufacturerView.as_view(), name='manufacturers'),
    path('sales/', SaleView.as_view(), name='sales'),
    path('news/', NewsView.as_view(), name='news'),
    path('stories/', StoryView.as_view(), name='stories'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    path('notifications/', NotificationView.as_view(), name='notifications'),
    path('user_sales/', UserSaleView.as_view(), name='user_sales'),
    path('user_sales/<int:pk>', UserSaleDetailView.as_view(), name='user-sales-detail'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('order_details/', OrderDetailView.as_view(), name='order_details'),
    path('products/', ProductView.as_view(), name='products'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product-detail'),

    path('user_totals/', UserTotalStatusView.as_view(), name='user_totals'),
    path('user_bonuses/', UserCashbackHistoryVew.as_view(), name='user_bonuses'),
    path('top_products/', TopProductAPIView.as_view(), name='top_products'),
    path('similar_products/', SimilarProductView.as_view(), name='similar_products'),
    path('sale_products/', SaleProducts.as_view(), name='sale_products'),
    path('recommendation_products/', Recommendation.as_view(), name='recommendation_products'),

    path('check_promocode/', CheckPromoCode.as_view(), name='check_promocode'),

    path('qr_code/', QrCodeView.as_view(), name='qr_code'),

    path('cards/', CardView.as_view(), name='cards'),
    path('cards/<int:pk>', CardObject.as_view(), name='card-object'),
    path('add_order/', AddOrderView.as_view(), name='add-order'),

    path('users/', UserListView.as_view(), name='api-users'),
    path('user_cashback_history/', UserCashbackHistoryVew.as_view(), name='user-cashback-history'),
    path('user_recommendation/', UserRecommendation.as_view(), name='user-recommendation'),
    path('user_comment/', CommentView.as_view(), name='user-comment'),
    path('user_locations/', LocationView.as_view(), name='user-locations'),
    path('user_locations/<int:pk>', LocationDetail.as_view(), name='user-locations-detail'),

    path('check_last_month_sale/', CheckSaleUsers.as_view(), name='user-check_last_month_sale'),

    path('push_token/', PushTokenView.as_view(), name='push-token'),

]
