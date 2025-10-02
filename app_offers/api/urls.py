from django.urls import path

from app_offers.api.views import OffersView, OfferView, OfferDetailView

urlpatterns = [
    path('api/offers/', OffersView.as_view(), name='offers'),
    path('api/offers/<int:id>/', OfferView.as_view(), name='offer'),
    path('api/offerdetails/<int:id>/', OfferDetailView.as_view(), name='offer_details'),
]