from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AracViewSet, SurucuViewSet, GorevViewSet, 
    KilometreKaydiViewSet, HarcamaViewSet,
    dashboard_stats, recent_activities
)

router = DefaultRouter()
router.register(r'araclar', AracViewSet)
router.register(r'suruculer', SurucuViewSet)
router.register(r'gorevler', GorevViewSet)
router.register(r'kilometreler', KilometreKaydiViewSet)
router.register(r'harcamalar', HarcamaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/stats/', dashboard_stats, name='dashboard-stats'),
    path('dashboard/activities/', recent_activities, name='recent-activities'),
] 