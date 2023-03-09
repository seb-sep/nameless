from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
import re

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


class StudentManager(BaseUserManager):
    def _create_user(self, email: str, password, is_superuser: bool, is_staff: bool):
        """
        Create a new user with the given values. Helper method for create_user and create_superuser.
        """
        if not email:
            raise ValueError("Email address required")
        if not password:
            raise ValueError("Password required")
        if not self.is_neu_email(email):
            raise ValueError("Must give a valid Northeastern email address")
        
        now = timezone.now()
        user = self.model(student_email=email, is_superuser=is_superuser, is_staff=is_staff)
        user.set_password(password)
        user.save(using=self._db)

        return user


    
    def create_user(self, email: str, password: str):
        """
        Create and save a student user with the given email.
        This email must be a valid Northeastern email address.
        """
        return self._create_user(email, password, False, False) 

    def create_superuser(self, email: str, password: str):
        return self._create_user(email, password, True, True)


    def is_neu_email(self, email: str) -> bool:
        """
        Validate whether the given email is a valid NEU Outlook or Gmail email.
        """
        return re.compile(r"^[a-zA-Z]+.[a-zA-Z]+@(northeastern|husky.neu).edu$").match(email) != None



class StudentAccount(AbstractBaseUser, PermissionsMixin):
    """A model class for representing a student account in the database."""

    student_email = models.EmailField(unique=True)
    num_infractions = models.IntegerField(default=0)
    USERNAME_FIELD = 'student_email'
    EMAIL_FIELD = 'student_email'
    REQUIRED_FIELDS = []
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    #TODO: Functionality for banning accounts when too many malicious messages
    #by setting this to false

    objects = StudentManager()
    
    def __str__(self):
        """Return a string representation of the student account: the email."""

        return self.student_email


class Message(models.Model):
    """A model class for representing an anonymous message from a student to a teacher of a class."""

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message_body = models.TextField()
    is_malicious = models.BooleanField(default=False)

