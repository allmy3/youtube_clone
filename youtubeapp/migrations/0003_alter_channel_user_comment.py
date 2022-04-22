# Generated by Django 4.0.3 on 2022-04-11 06:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('youtubeapp', '0002_video_channel_video_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_channel', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Содержимое')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='youtubeapp.comment', verbose_name='Родительский комментарий')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор коммента')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='youtubeapp.video', verbose_name='Видео-ролик')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['-created'],
            },
        ),
    ]