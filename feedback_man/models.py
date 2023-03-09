from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings

# Create your models here.

class Teacher(models.Model):
    """A model class for representing teachers in the database.
    Shares a many-to-many relationship with the Course table."""


    teacher_name = models.CharField(max_length=256, unique=True)
    college = models.CharField(max_length=256)
    email = models.EmailField(max_length=256, unique=True)

    def __str__(self):
        """Return a string representation of the teacher: their name."""
        return self.teacher_name


class Course(models.Model):
    """A model class for representing a course in the database.
    Shares a many-to-many relationship with the Teacher table."""

    class Semester(models.TextChoices):
        FALL = 'FA'
        SPRING = 'SP'
        SUMMER_1 = 'S1'
        SUMMER_2 = 'S2'

    class_name = models.CharField(max_length=256)
    semester = models.CharField(
        max_length=2,
        choices=Semester.choices,
    )
    year = models.IntegerField(null=True)
    course_num = models.IntegerField(null=True)
    subject = models.CharField(max_length=256)
    teachers = models.ManyToManyField(Teacher)

    def __str__(self):
        """Return a string representation of the course: the course number and name."""
        return f"{self.course_num} {self.class_name}"


class StudentAccount(AbstractBaseUser):
    """A model class for representing a student account in the database."""

    student_email = models.EmailField(unique=True)
    num_infractions = models.IntegerField(default=0)
    USERNAME_FIELD = 'student_email'
    EMAIL_FIELD = 'student_email'
    REQUIRED_FIELDS = []
    is_active = True 
    #TODO: Functionality for banning accounts when too many malicious messages
    #by setting this to false

    
    def __str__(self):
        """Return a string representation of the student account: the email."""

        return self.student_email


class Message(models.Model):
    """A model class for representing an anonymous message from a student to a teacher of a class."""

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message_body = models.TextField()
    is_malicious = models.BooleanField(default=False)

