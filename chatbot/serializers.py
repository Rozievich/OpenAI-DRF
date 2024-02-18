from rest_framework.serializers import ModelSerializer, CharField, ReadOnlyField
from .models import Chat
from .utils.openchat import ChatBotAI

class ChatModelSerializer(ModelSerializer):
    message = CharField(max_length=600, write_only=True)
    thread_id = ReadOnlyField()
    user_id = ReadOnlyField()

    class Meta:
        model = Chat
        fields = '__all__'
    
    def create(self, validated_data):
        message = validated_data.pop('message')
        user = self.context['request'].user
        thread = ChatBotAI().create_thread(content=message)
        validated_data['thread_id'] = thread.id
        validated_data['user_id'] = user
        return super().create(validated_data)
