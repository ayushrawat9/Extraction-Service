from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ExtractedTextViewSet 
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'extracted_text', ExtractedTextViewSet, basename='text')

urlpatterns = [
    path('extract', views.extract, name='extract'),
    path('', include(router.urls))
]