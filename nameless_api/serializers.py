from rest_framework import serializers
from feedback_man.models import Message, Teacher 

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
            model = Teacher
            fields = '__all__'