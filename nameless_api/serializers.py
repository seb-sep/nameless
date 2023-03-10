from rest_framework import serializers
from feedback_man.models import Message 

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
