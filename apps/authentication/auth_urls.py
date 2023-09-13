from django.urls import path
from knox import views as knox_views
from .views import LoginView, PhoneVerify, GetNameView

urlpatterns = [
     path(r'phone_verify/', PhoneVerify.as_view(), name='phone_verify'),
     path(r'get_name/', GetNameView.as_view(), name='get_name'),
     path(r'login/', LoginView.as_view(), name='knox_login'),
     path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
]

