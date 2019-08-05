import os, sys
import csv

# proj_path = "/home/jun/learninglab/"
# # This is so Django knows where to find stuff.
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learninglab.settings.production")
# sys.path.append(proj_path)

###########################
# for 2019 summer project
proj_path = "/Users/Bambiz/Dev/git/voting-app-new/voting-app/"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learninglab.settings.local")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from accounts.models import Student, Major
from courses.models import Section, Group

User = get_user_model()  

### group or user? ###
switch = 1

### Course Info ###
year = 2019
# title = "EM 1"
title = "Web-app development"

if switch == 1:
    #########################
    ##### create groups #####
    #########################
    """ 
    Sections are already created manually using admin mode

    """
    class_no = [41, 42, 43, 44]
    # number_of_groups = [16, 16, 16, 16]
    number_of_groups = [2, 2, 2, 2]

    # section = models.Section.objects.get(section_no=41, course__year=year, course__title=title)
    # models.Group.objects.create(section=section, group_no=2)

    for number in class_no:
        section = Section.objects.get(section_no=number, course__year=year, course__title=title)
        for g_number in range(number_of_groups[class_no.index(number)]):
            Group.objects.create(section=section, group_no=g_number + 1)

if switch == 2:
    #########################
    ##### create majors #####
    #########################
    with open("/Users/Bambiz/Dev/git/voting-app-new/voting-app/major_list.csv",encoding = 'UTF8') as f:
        majors = []
        for line in csv.reader(f):
            line = "".join(line)
            majors.append(line)

    for major in majors:
        Major.objects.create(title=major)

if switch == 3:
    #################################
    ##### create user instances ######
    #################################
    # import users from csv file
    # with open('/home/jun/Downloads/em1_2019_django_account.csv') as f:
    #     users = [tuple(line) for line in csv.reader(f)]

    # for 2019 summer project
    with open("/Users/Bambiz/Dev/git/voting-app-new/voting-app/accounts_list.csv", encoding = 'UTF8') as f:
        users = [tuple(line) for line in csv.reader(f)]
    # print(users)

    # create users
    for username, password, student_no, name, major, section, group in users:
        try:
            print('Creating user {0}.'.format(username))
            user = User.objects.create_user(username=username)
            user.set_password(password)
            user.is_student=True
            user.save()

            assert authenticate(username=username, password=password)
            print('User {0} successfully created.'.format(username))

            # create student - onetoneField with user
            student = Student(user=user)

            student.student_no = student_no
            student.name = name
            student.major = Major.objects.get(title=major)
            student.section = Section.objects.get(section_no=section, course__year=year, course__title=title)
            student.group = Group.objects.get(section__section_no=section, section__course__year=year, section__course__title=title, group_no=group)
            student.save()

        except:
            print('There was a problem creating the user: {0}.  Error: {1}.' \
                .format(username, sys.exc_info()[1]))