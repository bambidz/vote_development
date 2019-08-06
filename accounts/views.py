# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View
from django.views.generic.base import TemplateView
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
# from tablib import Dataset

from .forms import SignUpForm
# from .resources import StudentResource
from learninglab.decorators import student_required, teacher_required

from django.conf import settings # 추천!

from accounts.models import Student, User


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


@method_decorator(student_required, name='dispatch')
class StudentView(TemplateView):
    template_name = 'accounts/student.html'


@method_decorator(teacher_required, name='dispatch')
class TeacherView(TemplateView):
    template_name = 'accounts/teacher.html'


def login_success(request):
    """
    Redirect users based on whether they are students or teachers.
    """
    if request.user.is_student:
        return redirect('votes:voting')
    else:
        return redirect('votes:list')

#class MyPageView(settings.AUTH_USER_MODEL, ListView):
#    __metaclass__= ListView()
#    model = self.request.user



class Student_MyPage(View):
    def get(self, request):

        ### Parse user_id
        user_id = request.user.get_username() #eirc8260


        ### Get the user Info 
        Info = self.get_student_info(user_id)


        ### Response
        return render(request, 'accounts/student_mypage.html', {'Info': Info})

    #TODO: 
    def get_student_info(self, user_id):
        std_list = Student.objects.all()
        for n in std_list:
            if n.get_username() == user_id:
                return n
                break;
        return None

