from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('my-channel/', my_channel, name='my_channel'),
    path('channel/<str:slug>/', get_channel, name='get_channel'),
    path('create-channel/', create_channel, name='create_channel'),
    path('watch/video/<int:video_id>/', watch_video, name='watch'),
    path('sub-or-unsub/<user_username>/<option>/', sub, name='follow'),
    path('update-channel-data/', UpdateChannelData.as_view(), name='upd_data'),
    path('video-management/', ChannelManagementPage.as_view(), name='management'),
    path('upload/', upload_view, name='upload'),
    path('like-<int:video_id>/', like, name='like'),
    path('update-video-<int:pk>/', UpdateVideoPage.as_view(), name='update_video'),
    path('delete-video-<int:pk>/', DeleteVideoPage.as_view(), name='delete_video'),
    path('subscribtions/', SubsctibtionsPage.as_view(), name='subs'),
]