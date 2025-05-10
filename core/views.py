from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Arac, Surucu, Gorev, KilometreKaydi, Harcama
from .serializers import AracSerializer, SurucuSerializer, GorevSerializer, KilometreKaydiSerializer, HarcamaSerializer

# Create your views here.

class AracViewSet(viewsets.ModelViewSet):
    queryset = Arac.objects.all()
    serializer_class = AracSerializer
    permission_classes = [IsAuthenticated]

class SurucuViewSet(viewsets.ModelViewSet):
    queryset = Surucu.objects.all()
    serializer_class = SurucuSerializer
    permission_classes = [IsAuthenticated]

class GorevViewSet(viewsets.ModelViewSet):
    queryset = Gorev.objects.all()
    serializer_class = GorevSerializer
    permission_classes = [IsAuthenticated]

class KilometreKaydiViewSet(viewsets.ModelViewSet):
    queryset = KilometreKaydi.objects.all()
    serializer_class = KilometreKaydiSerializer
    permission_classes = [IsAuthenticated]

class HarcamaViewSet(viewsets.ModelViewSet):
    queryset = Harcama.objects.all()
    serializer_class = HarcamaSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    try:
        # Temel istatistikler
        total_vehicles = Arac.objects.count()
        active_drivers = Surucu.objects.filter(aktif=True).count()
        
        # Son 30 günlük görevler
        thirty_days_ago = timezone.now() - timedelta(days=30)
        monthly_tasks = Gorev.objects.filter(baslangic_tarihi__gte=thirty_days_ago).count()
        
        # Son 30 günlük toplam harcama
        monthly_expenses = Harcama.objects.filter(
            tarih__gte=thirty_days_ago
        ).aggregate(total=Sum('tutar'))['total'] or 0
        
        return Response({
            'total_vehicles': total_vehicles,
            'active_drivers': active_drivers,
            'monthly_tasks': monthly_tasks,
            'monthly_expenses': float(monthly_expenses)
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_activities(request):
    try:
        # Son 10 aktiviteyi al
        activities = []
        
        # Son görevler
        recent_tasks = Gorev.objects.order_by('-created_at')[:5]
        for task in recent_tasks:
            activities.append({
                'type': 'task',
                'description': f"{task.arac.plaka} aracı için {task.surucu.ad} {task.surucu.soyad} sürücüsüne görev atandı",
                'date': task.created_at
            })
        
        # Son harcamalar
        recent_expenses = Harcama.objects.order_by('-created_at')[:5]
        for expense in recent_expenses:
            activities.append({
                'type': 'expense',
                'description': f"{expense.arac.plaka} aracı için {expense.tutar} TL {expense.tip} harcaması yapıldı",
                'date': expense.created_at
            })
        
        # Tüm aktiviteleri tarihe göre sırala
        activities.sort(key=lambda x: x['date'], reverse=True)
        
        return Response(activities[:10])  # En son 10 aktiviteyi döndür
    except Exception as e:
        return Response({'error': str(e)}, status=500)
