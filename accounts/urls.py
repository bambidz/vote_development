# accounts/urls.py
from django.urls import path

from .views import SignUp, StudentView, TeacherView, login_success


app_name = 'accounts'

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    path('login_success', login_success, name='login_success'),
    path('student_view', StudentView.as_view(), name='student_view'),
    path('teacher_view', TeacherView.as_view(), name='teacher_view'),
    #path('mypage', MyPageView.asview(), name='mypage'),
]