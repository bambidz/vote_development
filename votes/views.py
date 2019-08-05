# votes/views.py
# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, CreateView, UpdateView, View, DetailView
)
from django.core.exceptions import ObjectDoesNotExist
# from django.views.generic.edit import FormMixin
# import datetime
from django.utils import timezone
import pytz
# from django.db.models import Count, Q

from .models import Question, Response
from accounts.models import Student
from learninglab.decorators import student_required, teacher_required
from . import mixins
# from .forms import VoteForm


@method_decorator(teacher_required, name='dispatch')
class QuestionListView(ListView):
    model = Question
    

@method_decorator(teacher_required, name='dispatch')
class QuestionView(View):
    # model = Question
    def get(self, request, *args, **kwargs):
        response_list = Response.objects.filter(question = kwargs["pk"])
        student_list = Student.objects.filter(section = kwargs["se"]).order_by('group')
        question = get_object_or_404(Question, pk=kwargs["pk"])

        response_status = []

        for i in range(len(student_list)):
            response_status.append([])
            response_status[i].append(student_list[i])
            response_status[i].append(0)
            for j in range(len(response_list)):
                if response_list[j].student == response_status[i][0]:
                    response_status[i][1] = 1

        return render(request,
            "votes/question_detail.html",
            {"question": question, "response_status": response_status, "response_list" : response_list})

    def post(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs["pk"])
        if "_check_vote" in self.request.POST:
            print("Check Vote")
            question.is_active = True
            question.code = 1
            question.save()
        elif "_vote_again" in self.request.POST:
            print("Vote Again")
            question.code = 2
            question.save()
        elif "_plot" in self.request.POST:
            print("Plot")
            return redirect("votes:plot", pk=kwargs["pk"])
        elif "_list" in self.request.POST:
            print("list")
            # reset all parameters to zero
            # then go to QuestionListView
            qs = Question.objects.all()
            qs.update(is_active=False)
            qs.update(code=0)
            return HttpResponseRedirect(reverse("votes:list"))
       # elif "_status" in self.request.POST:
       # print("Get Status")
       #     return redirect("votes:status", pk=kwargs["pk"])
        return redirect("votes:detail", pk=kwargs["pk"], se=kwargs["se"])

    
# for voting count
def count_voting(request, pk):
    # print(pk)
    question = get_object_or_404(Question, pk=pk)
    # print(question)
    created_time = timezone.now() - timezone.timedelta(minutes=20)
    # print(created_time)
    print("count voting")
    r = Response.objects.filter(
        question__pk=pk,
        timestamp__gte=created_time)
        # student__section__section_no=41).count()
    vote1 = r.filter(vote1__isnull=False).count()
    vote2 = r.filter(vote2__isnull=False).count()
    # print(r)
    # print(vote1)
    data = {
                "vote1": vote1,
                "vote2": vote2,
            }
    return JsonResponse(data)

    
# @teacher_required
# def vote_question(request, question_pk):
#     # set all questions' state to deactive
#     # qs = Question.objects.all()
#     # qs.update(is_active=False)

#     try:
#         question = get_object_or_404(Question, pk=question_pk)
#         question.is_active = True
#         question.code = 1
#         question.save()
#         context = {'question': question}
#     except ObjectDoesNotExist:
#         print("Question number does not exist.")
#         # (To Do) show proper error messsage.

#     # if request.method == "GET":
#     #     request.GET.get("data")
#     if request.POST:
#         if "_check_vote" in request.POST:
#             # query for showing how many votes for the last 5 minutes
#             # created_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
#             created_time = timezone.now() - timezone.timedelta(minutes=20)
#             # print(created_time)
#             print(question.code)

#             r = Response.objects.filter(
#                 question__pk=question_pk,
#                 timestamp__gte=created_time)
#                 # student__section__section_no=41).count()
#             vote1 = r.filter(vote1__isnull=False).count()
#             vote2 = r.filter(vote2__isnull=False).count()
#             context = {
#                         'question': question,
#                         'vote1': vote1,
#                         'vote2': vote2,
#                     }
#             # return render(request, "votes/partial_results.html", context1)
#         elif "_plot" in request.POST:
#             return redirect("votes:plot", question_pk=question_pk)
#         elif "_vote_again" in request.POST:
#             question.code = 2
#             question.save()
#             # created_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
#             # created_time = timezone.now() - timezone.timedelta(minutes=5)
#         elif "_list" in request.POST:
#             question.is_active = False
#             question.code = 0
#             question.save()
#             return HttpResponseRedirect(reverse("votes:list"))

#     return render(request, "votes/question_detail.html", context)

@method_decorator(student_required, name='dispatch')
class ResponseCreateView(LoginRequiredMixin, mixins.SuccessMessageMixin, CreateView):
    model = Response
    fields = ('v_response', )
    success_message = "You have submitted your first vote! It's time to discuss."
    # queryset = VoteQuestion.objects.filter(is_active=True, code=1)

    def form_valid(self, form):
        print("first_vote")
        try:
            question = Question.objects.get(is_active=True, code=1)
        except ObjectDoesNotExist:
            print("Error")
            messages.success(self.request, "First vote is not ready. Please wait.")
            return redirect("votes:voting")

        try:
            response = Response.objects.get(question_id=question.id,
                student__student_no=self.request.user.student.student_no)
            messages.success(self.request, "You've already voted!")
            # print(self.object)    # None
            return redirect("votes:edit", pk=response.pk)
        except:
            form.instance.question = question
            form.instance.student = self.request.user.student
            form.instance.vote1 = form.cleaned_data['v_response']
            super().form_valid(form)
            # print(self.object)    # Response object (15)
            return redirect("votes:edit", pk=self.object.pk)

    # Problematic scenarios
    # 1. After the first vote, students are redirected to UpdateView.  At this point,
    #    they move back to votes/voting and vote again, then new instance of response created.
    #    (RESOLVED!)
    # 2. Did not submit the first vote and the question status is moved to 2nd vote.
    # 3. Similar to 1, students can vote again after log out and re-log in.
    #    (RESOLVED!)

@method_decorator(student_required, name='dispatch')
class ResponseUpdateView(LoginRequiredMixin, UpdateView):
    model = Response
    fields = ('v_response', )
   
    def form_valid(self, form):
        print("second_vote")
        try:
            Question.objects.get(is_active=True, code=2)
            form.instance.vote2 = form.cleaned_data['v_response']
            # form.instance.question2 = form.cleaned_data['question']
            messages.success(self.request, "You have submitted your second vote!")
            super().form_valid(form)
            return redirect("accounts:student_view")
        except ObjectDoesNotExist:
            messages.success(self.request, "Please wait. Second vote is not ready.")
            return redirect("votes:edit", pk=self.object.pk)

    # Problematic scenarios:
    # 1. With the information of edit:voting with pk, students can vote 
    #    1st & 2nd depending on the code status, regardless of the current question.


####### Plot voting results.
@teacher_required
def json_example(request, pk):
    # I just need to pass question_pk; do not need to get question object.
    # (To Do) Revise later.
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'votes/json_example.html', {'question': question})


@teacher_required
def chart_data(request, pk):
    # dataset = Passenger.objects \
    #     .values('ticket_class') \
    #     .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
    #             not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
    #     .order_by('ticket_class')
    # The queryset above generates a data in the following format:
    # [
    #     {'ticket_class': 1, 'survived_count': 200, 'not_survived_count': 123},
    #     {'ticket_class': 2, 'survived_count': 119, 'not_survived_count': 158},
    #     {'ticket_class': 3, 'survived_count': 181, 'not_survived_count': 528}
    # ]

    # question = get_object_or_404(Question, pk=question_pk)
    # created_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
    # print(created_time)
    created_time = timezone.now() - timezone.timedelta(minutes=20)

    dataset = [
    {'vote': 1, 
        'choice1': Response.objects.filter(vote1=1, question__pk=pk,
                    timestamp__gte=created_time).count(), 
        'choice2': Response.objects.filter(vote1=2, question__pk=pk,
                    timestamp__gte=created_time).count(),
        'choice3': Response.objects.filter(vote1=3, question__pk=pk,
                    timestamp__gte=created_time).count(),
        'choice4': Response.objects.filter(vote1=4, question__pk=pk,
                    timestamp__gte=created_time).count()
        },
    {'vote': 2, 
        'choice1': Response.objects.filter(vote2=1, question__pk=pk,
                    timestamp__gte=created_time).count(), 
        'choice2': Response.objects.filter(vote2=2, question__pk=pk,
                    timestamp__gte=created_time).count(),
        'choice3': Response.objects.filter(vote2=3, question__pk=pk,
                    timestamp__gte=created_time).count(),
        'choice4': Response.objects.filter(vote2=4, question__pk=pk,
                    timestamp__gte=created_time).count()
        }
    ]

    categories = list()
    choice1_series_data = list()
    choice2_series_data = list()
    choice3_series_data = list()
    choice4_series_data = list()

    for entry in dataset:
        categories.append('%s Vote' % entry['vote'])
        choice1_series_data.append(entry['choice1'])
        choice2_series_data.append(entry['choice2'])
        choice3_series_data.append(entry['choice3'])
        choice4_series_data.append(entry['choice4'])

        choice1_series = {
            'name': 'Choice1',
            'data': choice1_series_data,
            'color': 'green'
        }

        choice2_series = {
            'name': 'Choice2',
            'data': choice2_series_data,
            'color': 'red'
        }

        choice3_series = {
            'name': 'Choice3',
            'data': choice3_series_data,
            'color': 'blue'
        }

        choice4_series = {
            'name': 'Choice4',
            'data': choice4_series_data,
            'color': 'black'
        }

        chart = {
            'chart': {'type': 'bar'},
            'title': {'text': 'Voting Results'},
            'xAxis': {'categories': categories},
            'series': [choice1_series, choice2_series, choice3_series, choice4_series]
        }

    return JsonResponse(chart)



# Just for testing.
@method_decorator(teacher_required, name='dispatch')
class ResponseStatusView(ListView):
        def get(self, request, *args, **kwargs):
            response_list = Response.objects.filter(question = kwargs["pk"]).order_by('student')
            student_list = Student.objects.all()
            #question = get_object_or_404(Question, pk=kwargs["pk"])   
            return render(request,
                "votes/response_list.html",
                {"response_list": response_list,"student_list": student_list})