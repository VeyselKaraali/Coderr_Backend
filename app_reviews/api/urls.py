from django.urls import path

from app_reviews.api import views


urlpatterns = [
    path('api/reviews/', views.ReviewView.as_view(), name='reviews'),
    path('api/reviews/<int:id>/', views.ReviewView.as_view(), name='review'),
]