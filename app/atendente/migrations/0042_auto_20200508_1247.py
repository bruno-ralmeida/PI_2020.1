# Generated by Django 3.0.5 on 2020-05-08 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atendente', '0041_auto_20200508_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atendente',
            name='foto',
            field=models.ImageField(blank=True, upload_to='fotos/1588952837.842643'),
        ),
    ]
