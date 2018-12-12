from django.contrib import admin
from .models import *


class MemberAdmin(admin.ModelAdmin):
    fields = ('username','first_name','password','image','dob','match','email','gender','hobby')
    list_display = ('username','password')
    ordering = ['username']

admin.site.register(Hobby)
admin.site.register(Member, MemberAdmin)