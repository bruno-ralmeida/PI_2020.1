# Generated by Django 3.0.5 on 2020-04-19 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atendente', '0019_auto_20200417_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atendente',
            name='foto',
            field=models.ImageField(blank=True, upload_to='fotos/1587260330.852127'),
        ),
    ]