# Generated by Django 4.2.21 on 2025-05-10 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_arac_options_alter_gorev_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gorev',
            name='baslik',
            field=models.CharField(default='Görev', max_length=200),
        ),
        migrations.AddField(
            model_name='gorev',
            name='durum',
            field=models.CharField(choices=[('beklemede', 'Beklemede'), ('devam_ediyor', 'Devam Ediyor'), ('tamamlandi', 'Tamamlandı'), ('iptal_edildi', 'İptal Edildi')], default='beklemede', max_length=20),
        ),
    ]
