from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Applicant)
admin.site.register(models.Role)
admin.site.register(models.ApplicantRole)
