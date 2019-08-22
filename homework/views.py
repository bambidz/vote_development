# homework/views.py
import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, View
from learninglab.decorators import student_required, teacher_required
from django.conf import settings # 추천!
from django.core import serializers


from .models import *
from accounts.models import *
from courses.models import *

from django.utils import timezone


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
        type_no = self.request.GET.get('type')
        user_id = self.request.GET.get('user_id')
        hw_no = self.request.GET.get('hw_name')
        now = datetime.datetime.now()
        
        s_instance = get_student_info(user_id)
        h_instance = Homework.objects.get(title=hw_no) #section을 타고 course를 타야한다.
        
        ### It Not exist, make new one 
        if not HomeworkTraker.objects.filter(Student=s_instance.pk, Homework=h_instance.pk).exists():
            print("Nonono")
            new_row = HomeworkTraker(Student=s_instance, Homework=h_instance)
            new_row.save()


        if type_no == "hw":
            
            ### Get the Start Time
            print(user_id,  "START on HW ", hw_no," AT :", now)


            row = HomeworkTraker.objects.get(Student=s_instance.pk, Homework=h_instance.pk)    
            if row.start_time == None:
                row.start_time = now
                row.save()


        elif type_no == "video_1":

            ### Get the Start Time
            print(user_id,  "START on Video 1 of  ", hw_no," AT :", now)        


            row = HomeworkTraker.objects.get(Student=s_instance.pk, Homework=h_instance.pk)    
            if row.start_time_video_1 == None:
                row.start_time_video_1 = now
                row.save()

        
        elif type_no == "video_2":
            print("video 2 start")
            ### Get the Start Time
            print(user_id,  "START on Video 2 of ", hw_no," AT :", now)


            row = HomeworkTraker.objects.get(Student=s_instance.pk, Homework=h_instance.pk)    
            if row.start_time_video_2 == None:
                row.start_time_video_2 = now
                row.save()


        elif type_no == "video_3":
            print("video 2 start")
            ### Get the Start Time
            print(user_id,  "START on Video 2 of ", hw_no," AT :", now)


            row = HomeworkTraker.objects.get(Student=s_instance.pk, Homework=h_instance.pk)    
            if row.start_time_video_3 == None:
                row.start_time_video_3 = now
                row.save()

        return HttpResponse(status=200)



class HomeworkEndView(View):
    def get(self, request):
        print("Called of Endddddd=====================")
        
        return HttpResponse(status=200)


def get_student_info(user_id):
    std_list = Student.objects.all()
    for n in std_list:
        if n.get_username() == user_id:
            return n
            break;
    return None


def HomeworkAllList(request, hw_no):
    ### return homework list
    print(hw_no)
    hw_list = Homework.objects.filter(Course_id = hw_no)
    serialized_queryset = serializers.serialize('json', hw_list)

    return JsonResponse(serialized_queryset, safe=False)



def HomeworkCheckList(request, course_id, hw_no):
    print(course_id, hw_no)

    ### Get Section from Course 
    sec_list = Section.objects.filter(course= course_id).values_list('pk', flat=True)
    print(sec_list[0])

    ### Get all Students in this Course
    std_list = Student.objects.filter(section_id=sec_list[0]) | Student.objects.filter(section_id=sec_list[1]) | Student.objects.filter(section_id=sec_list[2]) | Student.objects.filter(section_id=sec_list[3])
    print(len(std_list))


    ### Get H/W time from tracker DB

    '''
    for std_list
        get corresponding hw db
        append to list
    
    make json

    '''


    return None




class HomeworkTrackerView(View):
    def get(self, request):
        course_list = Course.objects.all()

        return render(request, 'homework/homework_tracker.html', {'course_list':course_list})
