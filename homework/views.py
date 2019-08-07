# homework/views.py

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View
from django.views.generic.base import TemplateView
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from learninglab.decorators import student_required, teacher_required

from django.conf import settings # 추천!

from datetime import datetime
#from accounts.models import Student, User

from .models import *
from accounts.models import *


class HomeworkListView(View):
    def get(self, request, *args, **kwargs):
        
        ### Who is user?
        user_id = request.user.get_username()
        student = get_student_info(user_id)
        #TODO : 여기서 section_id 로 Section Table에서 해당하는 Course ID를 GET
        print(student.section_id)

        #TODO: get the submit link form where?
        ### Get homework list for the user
        hm = Homework.objects.all() #TODO: 여기에 Course ID로 filtering


        
        return render(request, 'homework/homework_list2.html', {'homework_list': hm})




### Django Model API : http://pythonstudy.xyz/python/article/310-Django-%EB%AA%A8%EB%8D%B8-API

### Handle the request FROM ajax 
class HomeworkStartView(View):
    def get(self, request):
        
        ### Parse Params from url -> user_id & hw No 
        user_id = self.request.GET.get('user_id')
        hw_no = self.request.GET.get('hw_name')

        
        ### Get the Start Time
        now = datetime.now()
        print(user_id,  "START on HW ", hw_no," AT :", now)
        

        s_instance = get_student_info(user_id)
        h_instance = Homework.objects.get(title=hw_no) #section을 타고 course를 타야한다.


        ### Save the info in DB(HomeworkTraker)
        ht = HomeworkTraker(Student = s_instance, Homework = h_instance, start_time=datetime.now(), end_time=datetime.now())
        ht.save()

        return HttpResponse(status=200)


def get_student_info(user_id):
    std_list = Student.objects.all()
    for n in std_list:
        if n.get_username() == user_id:
            return n
            break;
    return None