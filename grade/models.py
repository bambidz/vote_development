
from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Group, Section, Course
from accounts.models import Student


class Grade(models.Model):
   student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False, related_name='Grade.student+', unique=True)

   middle_score = models.IntegerField(null=True)
   
   final_score = models.IntegerField(null=True)
   
   attendance_score = models.IntegerField(null=True)
   
   total_web_work_score = models.IntegerField(null=True)
   
   total_pre_class_score = models.IntegerField(null=True)



