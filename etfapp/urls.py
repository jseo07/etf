from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('live_search/', views.live_search, name='live_search'),
    path('<str:symbol>/', views.result, name='result'),
]
