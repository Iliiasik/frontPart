from django.contrib import admin
from applications.helpcenter.models import *

admin.site.register(Questions)
admin.site.register(Complaint)
admin.site.register(SendProblem)
