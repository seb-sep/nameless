from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils import timezone
import re
import functools

class StudentManager(BaseUserManager):
    """
    Custom manager for student user class.
    """
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
    
class TeacherManager(models.Manager):
    def search_teacher_name(self, name: str):
        """
        Search for teachers matching the given name in the database.
        Returns a QuerySet of all teachers who fit the search.
        """
        return self.filter(teacher_name__iregex=regex_token_search(name))
    
class CourseManager(models.Manager):
    def search_course_name(self, name: str):
        """"
        Search for courses matching the given name in the database.
        Returns a QuerySet of all courses who fit the search.
        """
        return self.filter(course_name__iregex=regex_token_search(name))



def regex_token_search(query: str):
    """
    Create a regular expression for searching the database by matching for zero or more characters between
    each token in the query.
    """
    #regex of all tokens in the passed name with zero or more characters in between/on the ends of each
    return functools.reduce(lambda regex, token: regex + re.escape(token+"*+"), query.split(), r"*+")