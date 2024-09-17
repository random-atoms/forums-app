from django.db import models

# Create your models here.

class User(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    username = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post by {self.user.username} in {self.room.name}'
