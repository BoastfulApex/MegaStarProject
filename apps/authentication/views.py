from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from rest_framework.response import Response
from rest_framework import generics

from .models import MegaUser
from .serializers import PhoneVerifySerializer


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
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class PhoneVerify(generics.CreateAPIView):
    queryset = MegaUser.objects.all()
    serializer_class = PhoneVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = MegaUser.objects.get(phone=request.data["phone"])
            user.generate_otp()

            return Response({"status": "created"})
