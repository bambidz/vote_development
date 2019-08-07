from django.db import models
from courses.models import Course
from accounts.models import Student

class Homework(models.Model):
    title = models.CharField(max_length=255)
    contents = models.FileField(upload_to='homework/')
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    
    is_active = models.IntegerField(default=0)


    def __str__(self):
        return f"(Homework {self.title})"


class HomeworkTraker(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    Homework = models.ForeignKey(Homework, on_delete=models.CASCADE, null=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    #TODO: Constraints 추가하기
    # Student field와 Homework field 를 합쳐서 Unique Key로 만든다.
