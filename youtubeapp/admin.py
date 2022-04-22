from django.contrib import admin

from .models import Video, Channel, Category, Comment, Like, Subscribe


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'visibility']
    list_display_links = ['title']
    search_fields = ['title', 'description']
    list_filter = ['visibility']


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_display_links = ['name']
    search_fields = ['name']


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Subscribe)