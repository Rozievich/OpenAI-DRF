from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ChatModelSerializer
from .models import Chat

class ChatListCreateAPIView(ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatModelSerializer
    permission_classes = (IsAuthenticated, )
