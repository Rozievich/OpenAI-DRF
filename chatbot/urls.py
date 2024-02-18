from django.urls import path
from .views import ChatListCreateAPIView

urlpatterns = [
    path('chat/', ChatListCreateAPIView.as_view(), name='chat-list')
]
