# Generated by Django 5.1.3 on 2024-12-06 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files2', '0002_appfeatures'),
    ]

    operations = [
        migrations.AddField(
            model_name='appfeatures',
            name='prediction',
            field=models.BooleanField(default=False),
        ),
    ]
