from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from app_authentication.api import views

urlpatterns = [
    path('api/registration/', views.RegistrationView.as_view(), name='registration'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]