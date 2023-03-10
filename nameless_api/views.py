from rest_framework.response import Response
from rest_framework.decorators import api_view
from feedback_man.models import Message, Teacher, Course
from .serializers import MessageSerializer, TeacherSerializer, CourseSerializer

@api_view(['GET'])
def getData(request):
    student = {'emeail':"sepulveda.s@northeastern.edu"}
    return Response(student)

@api_view(['GET'])
def searchTeacher(request, name):
    """
    Return a JSON response of all teachers in the database who match the given name.
    """
    teachers = Teacher.objects.search_teacher_name(name)
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def searchCourse(request, name):
    """
    Return a JSON response of all courses in the database who match the given course.
    """
    courses = Course.objects.search_course_name(name)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTeacher(request, pk):
    """
    Return a JSON response of the teacher with the given email.
    """

    teacher = Teacher.objects.get(id=pk)
    serializer = TeacherSerializer(teacher)
    return Response(serializer.data)

@api_view(['POST'])
def sendMessage(request):
    """
    Send an anonymous message to the teacher from the student,
    as specified by the message body.
    """

    serializer = MessageSerializer(data=request.data)

    if serializer.is_valid():
        #Save to the database and send the message contents to the teacher's email
        serializer.save().email_message()
