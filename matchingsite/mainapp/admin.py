from django.contrib import admin
from .models import *

class MemberAdmin(admin.ModelAdmin):
    fields = ('username','password','email','gender','hobby')
    list_display = ('username','password','hobbies_count')
    ordering = ['username']

admin.site.register(Hobby)
admin.site.register(Member, MemberAdmin)