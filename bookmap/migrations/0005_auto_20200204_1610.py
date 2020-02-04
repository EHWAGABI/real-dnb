# Generated by Django 2.2.6 on 2020-02-04 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookmap', '0004_auto_20200203_1358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={},
        ),
        migrations.RemoveField(
            model_name='tag',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='img',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='like',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='private',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='user',
        ),
        migrations.CreateModel(
            name='Thema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField()),
                ('img', models.ImageField(blank=True, null=True, upload_to='thema/')),
                ('private', models.BooleanField(default=False)),
                ('like', models.ManyToManyField(related_name='like', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.AddField(
            model_name='bookstore',
            name='thema_set',
            field=models.ManyToManyField(blank=True, to='bookmap.Thema'),
        ),
    ]