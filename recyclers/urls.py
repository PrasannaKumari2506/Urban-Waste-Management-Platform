from django.urls import path
from . import views

app_name = 'recyclers'

urlpatterns = [
    path('dashboard/', views.recycler_dashboard, name='dashboard'),
    path('pickup-requests/', views.pickup_requests, name='pickup_requests'),
    path('pickup/<int:pk>/', views.pickup_detail, name='pickup_detail'),
    path('pickup/<int:pk>/accept/', views.accept_pickup, name='accept_pickup'),
    path('pickup/<int:pk>/complete/', views.complete_pickup, name='complete_pickup'),
    path('history/', views.pickup_history, name='pickup_history'),
    path('notifications/', views.notifications, name='notifications'),
    path('reviews/', views.reviews, name='reviews'),
    path('earnings/', views.earnings_stats, name='earnings_stats'),
    path('guidelines/', views.recycling_guidelines, name='recycling_guidelines'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]





















