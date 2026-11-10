
import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def signup(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required."}, status=405)

    try:
        data = json.loads(request.body)

        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
        confirm_password = data.get("confirm_password", "")

        if not username or not email or not password:
            return JsonResponse({"error": "All fields are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists."}, status=400)

        if password != confirm_password:
            return JsonResponse({"error": "Passwords do not match."}, status=400)

        validate_password(password)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return JsonResponse({
            "message": "Account created successfully!",
            "username": user.username
        }, status=201)

    except ValidationError as error:
        return JsonResponse({"error": error.messages}, status=400)

    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid request data."}, status=400)


@require_POST
def user_login(request):
    try:
        data = json.loads(request.body)

        username = data.get("username", "")
        password = data.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            return JsonResponse({
                "message": "Login successful!",
                "username": user.username
            })

        return JsonResponse({
            "error": "Invalid username or password."
        }, status=400)

    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid request data."}, status=400)


@require_POST
def user_logout(request):
    logout(request)

    return JsonResponse({"message": "Logged out successfully!"})


def current_user(request):
    if request.user.is_authenticated:
        return JsonResponse({
            "authenticated": True,
            "username": request.user.username
        })

    return JsonResponse({"authenticated": False})


@require_POST
def delete_account(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Please login first."}, status=401)

    user = request.user
    logout(request)
    user.delete()

    return JsonResponse({"message": "Account deleted successfully!"})
