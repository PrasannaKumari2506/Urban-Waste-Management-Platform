from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('classifier/', views.waste_classifier, name='waste_classifier'),
    path('classifier/result/', views.classify_image, name='classify_image'),
    #path('how-it-works/', views.how_it_works, name='how_it_works'),
]
