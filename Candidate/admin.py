from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Candidate)
admin.site.register(Branch)
admin.site.register(College)
