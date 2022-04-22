from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import NewChannelAndUpdateChannelForm, NewVideoForm, NewCommentForm
from .models import Video, Channel, Category, Subscribe, Like, Comment

from youtube.utils import CheckAuthorMixin

User = get_user_model()


def index(request):
    videos = Video.objects.all()
    context = {
        'videos': videos,
    }
    return render(request, 'index.html', context)


@login_required
def my_channel(request):
    channel = Channel.objects.filter(user=request.user).first()
    if not channel:
        return redirect('create_channel')
    videos = Video.objects.filter(channel=channel)
    subscribers_count = channel.user.subscribe_user.count()
    context = {
        'channel': channel,
        'videos': videos,
        'subscribers_count': subscribers_count
    }
    return render(request, 'channel.html', context)


def get_channel(request, slug):
    channel = get_object_or_404(Channel, slug=slug)
    if request.user.is_authenticated:
        if Subscribe.objects.filter(subscriber=request.user, subscribe_user=channel.user).exists():
            is_sub = True
        else:
            is_sub = False
    else:
        is_sub = None
    videos = Video.objects.filter(channel=channel)
    subscribers_count = channel.user.subscribe_user.count()
    context = {
        'channel': channel,
        'videos': videos,
        'is_sub': is_sub,
        'subscribers_count': subscribers_count
    }
    return render(request, 'channel.html', context)


@login_required()
def create_channel(request):
    if request.user.user_channel.exists():
        return redirect('my_channel')
    else:
        if request.method == 'POST':
            form = NewChannelAndUpdateChannelForm(request.POST)
            if form.is_valid():
                new_channel = form.save(commit=False)
                new_channel.user = request.user
                new_channel.save()
                return redirect('index')
        else:
            form = NewChannelAndUpdateChannelForm()

        return render(request, 'update.html', {'form': form, 'title': 'Создать канал', "h3": "У вас нет канала, создать:"})


def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    context = {
        'video': video,
    }

    if request.user.is_authenticated:
        if Like.objects.filter(user=request.user, video=video).exists():
            is_liked = True
        else:
            is_liked = False

        if request.method == 'POST':
            form = NewCommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.video = video
                new_comment.save()
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            form = NewCommentForm()

        context['form'] = form
        context['is_liked'] = is_liked

    return render(request, 'video.html', context)


@login_required()
def sub(request, user_username, option):
    subscribe_user = get_object_or_404(User, username=user_username)
    try:
        s, created = Subscribe.objects.get_or_create(subscriber=request.user, subscribe_user=subscribe_user)
        if int(option) == 0:
            s.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    except User.DoesNotExist:
        return redirect(request.META.get('HTTP_REFERER'))


class UpdateChannelData(LoginRequiredMixin, UpdateView):
    template_name = 'update.html'
    form_class = NewChannelAndUpdateChannelForm
    model = Channel

    def get_object(self):
        channel = Channel.objects.get(user=self.request.user)
        return channel

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Изменение данных канала'
        context['h3'] = 'Изменение данных канала'
        return context


class ChannelManagementPage(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, user=request.user)
        objects = Video.objects.filter(channel=channel)
        context = {
            'objects': objects
        }
        return render(request, 'management.html', context)


@login_required()
def upload_view(request):
    user = request.user
    channel = get_object_or_404(Channel, user=user)

    if request.method == 'POST':
        form = NewVideoForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['video_file']
            new_video = form.save(commit=False)
            new_video.channel = channel
            new_video.file = file
            new_video.save()
            return redirect('index')
    else:
        form = NewVideoForm()

    return render(request, 'upload.html', {'form': form})


@login_required()
def like(request, video_id):
    user = request.user
    video = get_object_or_404(Video, id=video_id)
    current_video_likes = video.likes

    if Like.objects.filter(user=user, video=video).exists():
        Like.objects.filter(user=user, video=video).delete()
        current_video_likes -= 1
    else:
        Like.objects.create(user=user, video=video)
        current_video_likes += 1

    video.likes = current_video_likes
    video.save()
    return redirect(request.META.get('HTTP_REFERER'))


class UpdateVideoPage(CheckAuthorMixin, UpdateView):
    template_name = 'update.html'
    model = Video
    fields = ['title', 'description', 'visibility', 'thumbnail']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Редактирование видео ролика'
        return context


class DeleteVideoPage(CheckAuthorMixin, DeleteView):
    template_name = 'delete.html'
    model = Video
    context_object_name = 'video'

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Удаление видео ролика'
        object = self.get_object()
        context['object'] = object.title
        return context


class SubsctibtionsPage(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        subs = Subscribe.objects.filter(subscriber=request.user)
        context = {
            'subs': subs
        }
        return render(request, 'subs.html', context)