from django.db import models
from django.urls import reverse

from youtubeapp.models import Channel


class MonologuePhotoContent(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name='Канал', related_name='m_photos')
    image = models.ImageField(upload_to='monologue/')

    def __str__(self):
        return self.pk

    class Meta:
        verbose_name = 'фото для монолога'
        verbose_name_plural = 'Фотки монологов'


class MonologuePost(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name='Канал', related_name='monologues')
    text = models.TextField("Текст")
    created = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(MonologuePhotoContent, verbose_name='Фотки', blank=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('monologue', args=[self.channel.slug])

    class Meta:
        verbose_name = 'Монолог'
        verbose_name_plural = 'Монологи'