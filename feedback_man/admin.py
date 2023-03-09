from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StudentAccount

# Register your models here.

#Switching default user to StudentAccount class
admin.site.register(StudentAccount)

