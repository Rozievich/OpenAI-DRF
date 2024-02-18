from rest_framework.serializers import ModelSerializer
from .models import Chat
from .utils.openchat import create_asistant, create_thread, create_run, get_run

class ChatModelSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
    
    def create(self, validated_data):
        message = validated_data.get('message', None)
        if not validated_data.get('asistant_id', None):
            asistant = create_asistant()
        if not validated_data.get('thread_id', None):
            thread = create_thread(message=message)
        run = create_run(thread_id=thread, asistant_id=asistant)
        response = get_run(thread_id=thread, run_id=run)
        validated_data['asistant_id'] = asistant
        validated_data['thread_id'] = thread
        return super().create(validated_data)