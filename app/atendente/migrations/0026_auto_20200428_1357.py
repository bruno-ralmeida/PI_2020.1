# Generated by Django 3.0.5 on 2020-04-28 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atendente', '0025_auto_20200428_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atendente',
            name='foto',
            field=models.ImageField(blank=True, upload_to='fotos/1588092986.770368'),
        ),
    ]