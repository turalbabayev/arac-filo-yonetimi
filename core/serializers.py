from rest_framework import serializers
from .models import Arac, Surucu, Gorev, KilometreKaydi, Harcama

class AracSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arac
        fields = '__all__'

class SurucuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surucu
        fields = '__all__'

class GorevSerializer(serializers.ModelSerializer):
    arac_plaka = serializers.CharField(source='arac.plaka', read_only=True)
    surucu_adi = serializers.SerializerMethodField()

    def get_surucu_adi(self, obj):
        return f"{obj.surucu.ad} {obj.surucu.soyad}"

    class Meta:
        model = Gorev
        fields = ['id', 'baslik', 'arac', 'surucu', 'baslangic_tarihi', 'bitis_tarihi', 
                 'aciklama', 'durum', 'created_at', 'arac_plaka', 'surucu_adi']

class KilometreKaydiSerializer(serializers.ModelSerializer):
    class Meta:
        model = KilometreKaydi
        fields = '__all__'

class HarcamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harcama
        fields = '__all__' 