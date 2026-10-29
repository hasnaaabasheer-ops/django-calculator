from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import SignupForm


def signup(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username).exists():

                form.add_error(
                    "username",
                    "Username already exists."
                )

            else:

                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                return redirect("login")

    else:

        form = SignupForm()

    return render(
        request,
        "accounts/signup.html",
        {"form": form}
    )


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("calculator")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "accounts/login.html"
    )


def user_logout(request):

    logout(request)

    return redirect("login")


@login_required
def delete_account(request):

    if request.method == "POST":

        user = request.user

        logout(request)

        user.delete()

        return redirect("login")

    return redirect("calculator")