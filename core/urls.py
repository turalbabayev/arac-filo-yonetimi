from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('dashboard/activities/', views.recent_activities, name='recent_activities'),

    # Araçlar
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),

    # Sürücüler
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/<int:pk>/', views.driver_detail, name='driver_detail'),

    # Görevler
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),

    # Kilometre Kayıtları
    path('mileages/', views.mileage_list, name='mileage_list'),
    path('mileages/<int:pk>/', views.mileage_detail, name='mileage_detail'),

    # Harcamalar
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/<int:pk>/', views.expense_detail, name='expense_detail'),
] 