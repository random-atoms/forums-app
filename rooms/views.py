import hashlib
from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Post, User
from django.views.decorators.csrf import csrf_exempt

def home(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/home.html', {'rooms': rooms})

@csrf_exempt
def create_room(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        room, created = Room.objects.get_or_create(name=name, defaults={'description': description})
        return redirect('room_detail', room_id=room.id)
    return render(request, 'rooms/create_room.html')

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    posts = Post.objects.filter(room=room).order_by('created_at')
    return render(request, 'rooms/room_detail.html', {'room': room, 'posts': posts})

@csrf_exempt
def post_message(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    ip_address = get_ip(request)
    username = generate_username_from_ip(ip_address)
    
    # Get or create user based on the IP and generated username
    user, created = User.objects.get_or_create(ip_address=ip_address, defaults={'username': username})

    if request.method == 'POST':
        content = request.POST.get('content')
        Post.objects.create(user=user, room=room, content=content)
        return redirect('room_detail', room_id=room.id)
    return redirect('room_detail', room_id=room.id)

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def generate_username_from_ip(ip_address):
    """
    Generate a consistent, unique username from the IP address using a hash function.
    """
    print(f"Captured IP Address: {ip_address}")  # Debugging line
    hash_object = hashlib.sha256(ip_address.encode())
    # Generate a short, readable username based on the hash
    username = f"User-{hash_object.hexdigest()[:8]}"
    return username

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Room, Post, User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import hashlib

@csrf_exempt
def delete_room(request, room_id):
    """
    View to delete a room only if the correct password is provided.
    """
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        # Get the password from the form
        entered_password = request.POST.get('password')

        # Check if the entered password matches the stored secret password
        if entered_password == settings.ROOM_DELETE_PASSWORD:
            room.delete()
            messages.success(request, "Room deleted successfully.")
            return redirect('home')
        else:
            messages.error(request, "Incorrect password. Room deletion failed.")
            return redirect('room_detail', room_id=room.id)

    return render(request, 'rooms/delete_room.html', {'room': room})
