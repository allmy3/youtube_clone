import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def channel_directory(instance, filename):
    return 'video_files/channel_{0}/{1}'.format(instance.channel.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(max_length=50, verbose_name='URL для категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Channel(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название канала')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user_channel')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_photo = models.ImageField(upload_to='phone_photos/', null=True, blank=True)
    slug = models.SlugField(max_length=200, verbose_name='URL для канала')
    description = models.TextField("Описание канала")
    categories = models.ManyToManyField(Category, blank=True, verbose_name='Категории канала')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('get_channel', args=[self.slug])

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'


class Video(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name='Канал', blank=True, null=True)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True, verbose_name='Видео-файл')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name='Название ролика')
    description = models.TextField("Описание")
    visibility = models.BooleanField(choices=((False, 'Приватный'), (True, 'Публичный')))
    thumbnail = models.ImageField(upload_to='thumbnails/', null=False)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('watch', args=[self.pk])

    class Meta:
        verbose_name = 'Видео-ролик'
        verbose_name_plural = 'Видео-ролики'
        ordering = ['-created']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор коммента', related_name='my_comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='Видео-ролик', related_name='comments')
    content = models.TextField("Содержимое")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " " + self.video.title

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='my_likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='Видео-ролик', related_name='video_likes')

    def __str__(self):
        return self.user.username + " " + self.video.title

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Subscribe(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='subscriber')
    subscribe_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='subscribe_user')

    def __str__(self):
        return self.subscriber.username + " sub on " + self.subscribe_user.username

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'