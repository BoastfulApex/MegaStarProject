from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":
        print("AAAAAAAAAAAA")
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
