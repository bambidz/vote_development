from django.db import models
from courses.models import Course


class Homework(models.Model):
    title = models.CharField(max_length=255)
    contents = models.FileField(upload_to='homework/')
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    
    is_active = models.IntegerField(default=0)


    def __str__(self):
        return f"(Homework {self.title})"

    # def get_absolute_url(self):
    #     return reverse('votes:detail', kwargs={'pk': self.pk, 'se': '41'})