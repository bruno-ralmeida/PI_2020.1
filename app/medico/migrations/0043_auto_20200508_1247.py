# Generated by Django 3.0.5 on 2020-05-08 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0042_auto_20200508_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='foto',
            field=models.ImageField(blank=True, upload_to='fotos/1588952878.266966'),
        ),
    ]
