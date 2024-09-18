from django.urls import path
from .views import create_room, post_message, room_detail, home, delete_room

urlpatterns = [
    path('', home, name='home'),
    path('create_room/', create_room, name='create_room'),
    path('room/<int:room_id>/', room_detail, name='room_detail'),
    path('post_message/<int:room_id>/', post_message, name='post_message'),
    path('delete_room/<int:room_id>/', delete_room, name='delete_room'),  # New URL for deleting rooms
]
