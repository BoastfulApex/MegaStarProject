from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.signals import user_logged_in, user_logged_out
from knox.models import AuthToken

from django.contrib.auth import login

from rest_framework import permissions
from knox.views import LoginView as KnoxLoginView

from rest_framework.response import Response
from rest_framework import generics

from .models import MegaUser, send_sms
from .serializers import PhoneVerifySerializer, PhoneAuthTokenSerializer, SetNameSerializer


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":
        if form.is_valid():
            phone = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(phone=phone, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = PhoneAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = self.get_post_response_data(request, token, instance)

        return Response(
            {"status": True,
             "code": 200,
             "data": data,
             "message": []}
        )


class PhoneVerify(generics.CreateAPIView):
    queryset = MegaUser.objects.all()
    serializer_class = PhoneVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = MegaUser.objects.get(phone=request.data["phone"])
            user.generate_otp()
            data = {
                'otp': user.otp,
                'name': user.first_name
            }
            # send_sms(phone=user.phone, otp=user.otp)
            return Response(
                {
                    "status": True,
                    "code": 200,
                    "data": data,
                    "message": []
                }
            )


class GetNameView(generics.CreateAPIView):
    queryset = MegaUser.objects.all()
    serializer_class = PhoneVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = MegaUser.objects.get(phone=request.data["phone"])
            name = user.first_name if user.first_name else None
            return Response(
                {
                    "status": True,
                    "code": 200,
                    "data": {'name': name},
                    "message": []
                }
            )


    queryset = MegaUser.objects.all()
    serializer_class = PhoneVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = MegaUser.objects.get(phone=request.data["phone"])
            user.generate_otp()
            data = {
                'otp': user.otp,
                'name': user.first_name
            }
            send_sms(phone=user.phone, otp=user.otp)
            return Response(
                {
                    "status": True,
                    "code": 200,
                    "data": data,
                    "message": []
                }
            )


class SetNameView(generics.CreateAPIView):
    queryset = MegaUser.objects.all()
    serializer_class = SetNameSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = MegaUser.objects.get(phone=serializer.validated_data["phone"])
            user.first_name = serializer.validated_data['first_name']
            user.save()
            data = {
                'phone': user.phone,
                'name': user.first_name
            }
            return Response(
                {
                    "status": True,
                    "code": 200,
                    "data": data,
                    "message": []
                }
            )

