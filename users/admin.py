from django.contrib import admin
from .models import Student, Librarian, Materials
# Register your models here.

admin.site.register(Student)
admin.site.register(Librarian)
admin.site.register(Materials)