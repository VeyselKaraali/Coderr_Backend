from django.urls import path

from app_authentication.api import views


urlpatterns = [
    path('api/registration/', views.RegistrationView.as_view(), name='registration'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/logout/', views.LogoutView.as_view(), name='logout'),
]