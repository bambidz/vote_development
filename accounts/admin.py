from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Student, Major


# Define an inline admin descriptor for Student model
# which acts a bit like a singleton
class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    fk_name = 'user'


# Define a new User admin
# class User(models.User):
#     inlines = (StudentInline,)
class CustomUserAdmin(UserAdmin):
    inlines = (StudentInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(Major)
#admin.site.register(User, CustomUserAdmin)

admin.site.register(User)
admin.site.register(Student)