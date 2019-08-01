# votes/models.py
from django.db import models
from django.urls import reverse

from courses.models import Lecture
from accounts.models import Student


class StatusManager(models.Manager):
    def no_vote(self):
        return self.get(code=0)

    def first_vote(self):
        return self.get(code=1)

    def second_vote(self):
        return self.get(code=2)
# After setting code, e.g. code = 1, we can retrieve it using
# VoteQuestion.objects.first_vote()


class Question(models.Model):
    title = models.CharField(max_length=255)
    prompt = models.CharField(max_length=255, blank=True)
    contents = models.ImageField(null=True, blank=True)
    code = models.IntegerField(default=0)
    is_active = models.IntegerField(default=0)
    answer = models.TextField(blank=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    # custom model manager
    objects = StatusManager()

    def __str__(self):
        return f"(Lecture {self.lecture.order}) {self.title}"

    def get_absolute_url(self):
        return reverse('votes:detail', kwargs={'pk': self.pk, 'se': '1'})


class Response(models.Model):
    CHOICE = [(1, 1), (2, 2), (3, 3), (4, 4)]   
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    contents = models.ImageField(null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    vote1 = models.IntegerField(choices=CHOICE, null=True)  # 1st vote for multiple choice question
    vote2 = models.IntegerField(choices=CHOICE, null=True)  # 2nd vote for multiple choice question
    answer1 = models.CharField(max_length=255, null=True)  # 1st simple answers
    answer2 = models.CharField(max_length=255, null=True)  # 2nd simple answers
    v_response = models.IntegerField(choices=CHOICE, default=1)  # temp. place holder for vote
    a_response = models.CharField(max_length=255, null=True)     # temp. place holder for simple answer
    timestamp = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     # Students can create a unique response for each question.
    #     unique_together =(("question", "student"),)

    def get_absolute_url(self):
        return reverse('votes:edit', kwargs={'pk': self.pk})

    def __str__(self):
        return f"(Lecture {self.question.title}) {self.student.name}, Group : {self.student.group}"