from django.urls import path

from app_offers.api.views import OfferListCreateView

urlpatterns = [
    path('api/offers/<int:id>/', views.ProfileDetailView.as_view(), name='offer_details_1'),
    path('api/offerdetails/<int:id>/', views.ProfileDetailView.as_view(), name='offer_details_2'),
    path('api/offers/', OfferListCreateView.as_view(), name='offers'),
]