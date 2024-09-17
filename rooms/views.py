from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Room, Post, User
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string

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
    user, created = User.objects.get_or_create(ip_address=ip_address, defaults={'username': f'User-{get_random_string(8)}'})

    if request.method == 'POST':
        content = request.POST.get('content')
        Post.objects.create(user=user, room=room, content=content)
        return redirect('room_detail', room_id=room.id)
    return redirect('room_detail', room_id=room.id)

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
