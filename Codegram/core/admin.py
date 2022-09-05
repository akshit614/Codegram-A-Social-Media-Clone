from cProfile import Profile
import imp
from django.contrib import admin
from .models import ProFil , Poost

# Register your models here.
admin.site.register(ProFil)
admin.site.register(Poost)

