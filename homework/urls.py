# courses/urls.py
from django.urls import path

from .views import *


app_name = 'homework'

urlpatterns = [
    path('', HomeworkListView.as_view(), name='homework_list'),
    path('api/v1/start', HomeworkStartView.as_view(), name='hw_start'),
    path('api/v1/end', HomeworkEndView.as_view(), name='hw_end'),
]
