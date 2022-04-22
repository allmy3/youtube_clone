from django.urls import path

from .views import *

urlpatterns = [
    path('<slug:channel_slug>/', monologues, name='monologue'),
    path('update-monologue/<int:pk>/', UpdateMonologue.as_view(), name='update_m'),
    path('delete-monologue/<int:pk>/', DeleteMonologue.as_view(), name='delete_m'),
]