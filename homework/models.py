from django.db import models
from courses.models import Course
from accounts.models import Student


class Homework(models.Model):
    title = models.CharField(max_length=255)

    contents = models.FileField(upload_to='homework/')
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    
    due_date = models.CharField(max_length=255, null=True)

    video_clip_name_1 = models.CharField(max_length=255, null=True)
    video_clip_link_1 = models.CharField(max_length=255, null=True)
    video_clip_name_2 = models.CharField(max_length=255, null=True)
    video_clip_link_2 = models.CharField(max_length=255, null=True)
    video_clip_name_3 = models.CharField(max_length=255, null=True)
    video_clip_link_3 = models.CharField(max_length=255, null=True)
    
    quetions_image = models.ImageField(upload_to="homework/", null=True)
    
    is_active = models.IntegerField(default=0)

    class Meta:
        unique_together = (('title', 'Course'),)

    def __str__(self):
        return f"(Homework {self.title})"

        


class HomeworkTraker(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    Homework = models.ForeignKey(Homework, on_delete=models.CASCADE, null=True)

    start_time = models.DateTimeField(null=True)
    start_time_video_1 = models.DateTimeField(null=True)
    start_time_video_2 = models.DateTimeField(null=True)
    start_time_video_3 = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    class Meta:
        unique_together =(('Student', 'Homework'),)
