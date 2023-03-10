from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from .managers import StudentManager, TeacherManager, CourseManager
from django.core.mail import send_mail
from googleapiclient import discovery
import json
from ...nameless_root import local_settings

# Create your models here.
# TODO: Test cases for model methods

class Teacher(models.Model):
    """A model class for representing teachers in the database.
    Shares a many-to-many relationship with the Course table."""


    teacher_name = models.CharField(max_length=256, unique=True)
    college = models.CharField(max_length=256)
    email = models.EmailField(max_length=256, unique=True, primary_key=True)

    objects = TeacherManager()

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

    objects = CourseManager()

    def __str__(self):
        """Return a string representation of the course: the course number and name."""
        return f"{self.course_num} {self.class_name}"




class StudentAccount(AbstractBaseUser, PermissionsMixin):
    """A model class for representing a student account in the database."""

    student_email = models.EmailField(unique=True, primary_key=True)
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
    
    def increment_infractions(self):
        """
        Increment the number of infractions committed by the student and
        return the new total.
        """

        self.num_infractions += 1
        self.save(update_fields=["num_infractions"])
        return self.num_infractions


class Message(models.Model):
    """A model class for representing an anonymous message from a student to a teacher of a class."""

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message_body = models.TextField()
    is_malicious = models.BooleanField(default=False)

    def email_message(self):
        """
        Check the message for malicious content. If it is malicious, mark as malicious and increment the student account's infractions.
        If it is not malicious, send the message as an email.

        Returns a dict with a status and message.
        """

        if self.is_malicious_msg():
            self.is_malicious = True
            self.save(update_fields=['is_malicious'])

            num_infractions = self.student.increment_infractions()

            return {"Rejected":f"This message contains toxic or offensive content and will not \
                    be sent to the teacher. Your account has sent {num_infractions} malicious messages."}
        else:
            send_mail("Message from one of your students", self.message_body, from_email=None, recipient_list=[self.teacher.email])
            return {"Success":"This message has been sent to the teacher."}

    def is_malicious_msg(self):
        """Check if this message is malicious or not."""

        attributes = {"TOXICITY": {},
                    "IDENTITY_ATTACK": {},
                    "INSULT": {}}

        client = discovery.build(
                    "commentanalzyer",
                    "v1alpha1",
                    developerKey=local_settings.perspective_api_key,
                    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                    static_discovery=False,
                )

        analyze_request = {
            "comment": {"text": self.message_body},
            "requestedAttributes": attributes
        }
        response = client.comments().analyze(body=analyze_request).execute()

        attribute_scores = json.loads(response)["attributeScores"]
        for score in attribute_scores:
            if score["summaryScore"]["value"] > 0.7:
                return True

        return False


