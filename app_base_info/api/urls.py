from django.urls import path

from app_base_info.api.views import BaseInfoView

urlpatterns = [
    path('api/base-info/', BaseInfoView.as_view(), name='base-info'),
]
