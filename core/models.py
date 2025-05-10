from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Arac(models.Model):
    KAYNAK_TIPI = [
        ('ozmal', 'Özmal'),
        ('kiralik', 'Kiralık'),
    ]
    plaka = models.CharField(max_length=20, unique=True)
    marka = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    yil = models.PositiveIntegerField()
    tip = models.CharField(max_length=50)
    kaynak_tipi = models.CharField(max_length=10, choices=KAYNAK_TIPI)
    mevcut_durum = models.CharField(max_length=50, default='havuzda')
    aciklama = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.plaka} - {self.marka} {self.model}"

class Surucu(models.Model):
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    ehliyet_no = models.CharField(max_length=20)
    kullanici = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    telefon = models.CharField(max_length=20, default="")
    aktif = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.ad} {self.soyad}"

class Gorev(models.Model):
    arac = models.ForeignKey(Arac, on_delete=models.CASCADE)
    surucu = models.ForeignKey(Surucu, on_delete=models.CASCADE)
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField(null=True, blank=True)
    aciklama = models.TextField(default="")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.arac.plaka} - {self.surucu.ad} {self.surucu.soyad}"

class KilometreKaydi(models.Model):
    arac = models.ForeignKey(Arac, on_delete=models.CASCADE)
    tarih = models.DateField()
    kilometre = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.arac} - {self.tarih} - {self.kilometre} km"

class Harcama(models.Model):
    HARCAMA_TIPI = [
        ('bakim', 'Bakım'),
        ('kasko', 'Kasko'),
        ('yakıt', 'Yakıt'),
        ('lastik', 'Lastik'),
        ('tamir', 'Tamir'),
    ]
    arac = models.ForeignKey(Arac, on_delete=models.CASCADE)
    tarih = models.DateField()
    tip = models.CharField(max_length=20, choices=HARCAMA_TIPI)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    aciklama = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.arac} - {self.tip} - {self.tutar} TL"
