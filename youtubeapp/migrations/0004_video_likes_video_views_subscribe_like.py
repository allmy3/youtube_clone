# Generated by Django 4.0.3 on 2022-04-11 07:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('youtubeapp', '0003_alter_channel_user_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribe_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_likes', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_likes', to='youtubeapp.video', verbose_name='Видео-ролик')),
            ],
            options={
                'verbose_name': 'Лайк',
                'verbose_name_plural': 'Лайки',
            },
        ),
    ]