from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    thread_id = models.CharField(max_length=80)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user_id.username

    class Meta:
        ordering = ['-created_at']


class Files(models.Model):
    file_id = models.CharField(max_length=128)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user_id.username
    
    class Meta:
        ordering = ['-created_at']
