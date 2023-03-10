from rest_framework import serializers
from feedback_man.models import Message, Teacher, Course

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    
    '''
    def __init__(self, *args, **kwargs):
         profile = kwargs.pop("profile", None)

         super().__init__(*args, **kwargs)
    '''
         
    class Meta:
            model = Teacher
            fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
     class Meta:
          model = Course  
          fields = '__all__'
    