# Generated by Django 5.0.1 on 2024-03-26 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0006_rename_servicio_id_imagenfase_servicio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagenfase',
            name='imagen_path',
        ),
        migrations.AddField(
            model_name='imagenfase',
            name='imagen',
            field=models.ImageField(null=True, upload_to='imagenes_bd/'),
        ),
    ]
