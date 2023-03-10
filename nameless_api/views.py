from rest_framework.response import Response
from rest_framework.decorators import api_view
from feedback_man.models import Message
from .serializers import MessageSerializer

@api_view(['GET'])
def getData(request):
    student = {'emeail':"sepulveda.s@northeastern.edu"}
    return Response(student)


