from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict_crop/', views.predict_crop, name='predict_crop'),
    # You can add other URL patterns here if needed
]
