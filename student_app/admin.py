from django.contrib import admin
from .models import Student, Faculty,Course

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)