from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('applicant/<id>', views.applicantPage, name='applicantPage'),
    path('role/<id>', views.rolePage, name='rolePage'),
    path('addApplicant', views.addApplicant, name='addApplicant'),
    path('addRole', views.addRole, name='addRole'),
    path('addApplicantRole/<id>', views.addApplicantRole, name='addApplicantRole'),
    path('addRoleApplicant/<id>', views.addRoleApplicant, name='addRoleApplicant'),
    path('editApplicant/<id>', views.editApplicant, name='editApplicant'),
    path('deleteApplicant/<id>', views.deleteApplicant, name='deleteApplicant'),
    path('deleteRole/<id>', views.deleteRole, name='deleteRole'),
    path('deleteApplicantRole/<applicantId>/<roleId>', views.deleteApplicantRole, name='deleteApplicantRole'),
    path('deleteRoleApplicant/<roleId>/<applicantId>', views.deleteRoleApplicant, name='deleteRoleApplicant'),
]