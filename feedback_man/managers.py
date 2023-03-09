from django.db import models
from django.contrib.auth.base_user import BaseUserManager
import re

class StudentManager(BaseUserManager):
    def create_user(self, email: str, password=None):
        """
        Create and save a student user with the given email.
        This email must be a valid Northeastern email address.
        """
        if not email:
            raise ValueError("Email address required")
        if not password:
            raise ValueError("Password required")
        if not self.is_neu_email(email):
            raise ValueError("Must give a valid Northeastern email address")
        
        user = self.model(student_email= email)
        user.set_password(password)
        user.save(using=self._db)

        return user


    def is_neu_email(self, email: str) -> bool:
        """
        Validate whether the given email is a valid NEU Outlook or Gmail email.
        """
        return re.compile(r"^[a-zA-Z]+.[a-zA-Z]+@(northeastern|husky.neu).edu$").match(email) != None

