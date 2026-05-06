from django.urls import path
from . import views

app_name = 'households'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pickup/request/', views.request_pickup, name='request_pickup'),
    path('pickup/history/', views.pickup_history, name='pickup_history'),
    path('pickup/<int:pk>/review/', views.add_review, name='add_review'),
    path('educational/', views.educational_content, name='educational_content'),
]
