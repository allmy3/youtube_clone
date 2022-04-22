from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.forms import TextInput

from youtubeapp.models import Channel
from .models import MonologuePhotoContent, MonologuePost

from youtube.utils import CheckAuthorMixin


def monologues(request, channel_slug):
    channel = get_object_or_404(Channel, slug=channel_slug)
    monologues = MonologuePost.objects.filter(channel=channel)
    MonologueForm = modelform_factory(MonologuePost, fields=['text'], widgets={'text': TextInput(attrs={'placeholder': 'Текст монолога'})})

    if request.method == 'POST':
        form = MonologueForm(request.POST)
        if form.is_valid():
            new_monologue = form.save(commit=False)
            new_monologue.channel = channel
            new_monologue.save()
            return redirect('monologue', channel_slug=channel.slug)
    else:
        form = MonologueForm()

    context = {
        'channel': channel,
        'monologues': monologues,
        'form': form
    }
    return render(request, 'monologue/index.html', context)


class UpdateMonologue(CheckAuthorMixin, UpdateView):
    template_name = 'update.html'
    model = MonologuePost
    fields = ['text']
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Обновление поста монолога'
        return context


class DeleteMonologue(CheckAuthorMixin, DeleteView):
    template_name = 'delete.html'
    model = MonologuePost
    success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Удаление монологового поста'
        object = self.get_object()
        context['object'] = object.text
        return context