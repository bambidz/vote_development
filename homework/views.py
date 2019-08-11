# homework/views.py
from datetime import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, View
from learninglab.decorators import student_required, teacher_required
from django.conf import settings # 추천!


from .models import *
from accounts.models import *
from courses.models import *


class HomeworkListView(View):
    def get(self, request, *args, **kwargs):
        
        ### Who is user?
        user_id = request.user.get_username()
        student = get_student_info(user_id)
        

        ### Get homework list for the user
        hm = Homework.objects.all() #TODO: 여기에 Course ID로 filtering


        # ### Make a Pre-filled Google Forms URL with user params
        # google_forms_url = "https://docs.google.com/forms/d/e/1FAIpQLSf2FEAl6FRZP3kaf5lVaXRU3NRqfmrh-9IIhjxm-weolROamQ/viewform"
        # name_field = "entry.1053894363"
        # std_id_field = "entry.1441140489"
        # section_field = "entry.580230306"
        # hw_no_field = "entry.383023472"
        
        # personal_url_params =  google_forms_url + "?" + \
        #                         name_field+"="+student.name + \
        #                         "&" + std_id_field + "=" + str(student.student_no) + \
        #                         "&" + section_field + "=" + str(Section.objects.get(pk = student.section_id).section_no) + \
        #                         "&" + hw_no_field + "="


        


        return render(request, 'homework/homework_list.html', {'homework_list': hm})




def HomeworkDetailView(request, no):
    user_id = request.user.get_username()
    student = get_student_info(user_id)
    
    #hw = Homework.objects.get(title=no, Course = get_user_course_id(user_id))
    hw = Homework.objects.get(title=no)
    

    ### Make a Pre-filled Google Forms URL with user params
    google_forms_url = "https://docs.google.com/forms/d/e/1FAIpQLSf2FEAl6FRZP3kaf5lVaXRU3NRqfmrh-9IIhjxm-weolROamQ/viewform"
    name_field = "entry.1053894363"
    std_id_field = "entry.1441140489"
    section_field = "entry.580230306"
    hw_no_field = "entry.383023472"
    
    personal_url_params =  google_forms_url + "?" + \
                            name_field+"="+student.name + \
                            "&" + std_id_field + "=" + str(student.student_no) + \
                            "&" + section_field + "=" + str(Section.objects.get(pk = student.section_id).section_no) + \
                            "&" + hw_no_field + "="

    return render(request, 'homework/homework_detail.html', {'hw':hw, 'google_forms_url':personal_url_params})




# def get_user_course_id(user_id):
#     std_list = Student.objects.all()
#     for n in std_list:
#         if n.get_username() == user_id:
#             n.section
            
#             return 3
#     return 3


### Django Model API : http://pythonstudy.xyz/python/article/310-Django-%EB%AA%A8%EB%8D%B8-API

### Handle the request FROM ajax 
class HomeworkStartView(View):
    def get(self, request):
        
        ### Parse Params from url
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



class HomeworkEndView(View):
    def get(self, request):
        
        return HttpResponse(status=200)


def get_student_info(user_id):
    std_list = Student.objects.all()
    for n in std_list:
        if n.get_username() == user_id:
            return n
            break;
    return None