from django.urls import path
from . import views

urlpatterns = [
    path('calculate/', views.calculator_api, name='calculator_api'),
]