from django.urls import path

from app_profile.api import views


urlpatterns = [
    path('api/profile/<int:id>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('api/profiles/business/', views.ProfileBusinessView.as_view(), name='profile_business'),
    path('api/profiles/customer/', views.ProfileCustomerView.as_view(), name='profile_customer'),
]