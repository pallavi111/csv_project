from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/<int:upload_id>/', views.upload_detail, name='upload_detail'),
]
