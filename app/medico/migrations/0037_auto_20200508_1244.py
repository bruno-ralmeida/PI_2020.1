# Generated by Django 3.0.5 on 2020-05-08 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0036_auto_20200508_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='foto',
            field=models.ImageField(blank=True, upload_to='fotos/1588952644.3246546'),
        ),
    ]
