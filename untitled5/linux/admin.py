from django.contrib import admin

from linux.models import Teacher
# Register your models here.


class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "sex",
        "subject",
        "telphone",
    ]


admin.site.register(Teacher, TeacherAdmin)
