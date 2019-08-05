# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

from courses.models import Group, Section


# User Model: https://wsvincent.com/django-referencing-the-user-model/
# Multiple User Types: https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Major(models.Model):
    title = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_no = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=255, null=True)
    major = models.ForeignKey(Major, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #    return reverse('votes:edit', kwargs={'pk': self.pk})


