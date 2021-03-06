# Generated by Django 2.2.6 on 2020-01-28 00:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookmap', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='like',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tag',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tag',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
