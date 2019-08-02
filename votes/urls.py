# votes/urls.py
from django.urls import path

from . import views


app_name = 'votes'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='list'),
    path('voting', views.ResponseCreateView.as_view(), name='voting'),
    path('edit/v<int:pk>', views.ResponseUpdateView.as_view(), name='edit'),
    path('q<int:pk>/<int:se>', views.QuestionView.as_view(), name='detail'),
    # path('q<int:question_pk>', views.vote_question, name='detail'),
    # path('ticket-class', views.ticket_class_view, name='ticket'),
    path('plot/q<int:pk>', views.json_example, name='plot'),
    path('plot/data<int:pk>/', views.chart_data, name='chart_data'),
    path('ajax/count<int:pk>', views.count_voting, name='counting'),
    # path('q<int:pk>/status', views.ResponseStatusView.as_view(), name='status'),
]