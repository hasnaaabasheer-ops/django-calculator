from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('user/', views.current_user),
    path('delete-account/', views.delete_account),
]