from django.shortcuts import redirect, render
from . import models
from django.db.models import Q


# Create your views here.
def home(request):
    applicants = models.Applicant.objects.all()
    roles = models.Role.objects.all()
    
    applicantsRoles = []
    for applicant in applicants:
        applicantsRoles.append(models.ApplicantRole.objects.filter(applicant__exact=applicant.id))    
    applicantsData = zip(applicants, applicantsRoles)
    
    rolesApplicants = []
    for role in roles:
        rolesApplicants.append(models.ApplicantRole.objects.filter(role__exact=role.id).order_by('status'))
    rolesData = zip(roles, rolesApplicants)
    
    return render(request, "index.html", {'applicantsData': applicantsData, 'rolesData': rolesData})

def applicantPage(request, id):
    applicant = models.Applicant.objects.get(id=id)
    if not applicant:
        return redirect('home')
    applicantRoles = models.ApplicantRole.objects.filter(applicant=id)
    rolesLeft = models.Role.objects.exclude(id__in=applicantRoles.values_list('role', flat=True)).count()
    return render(request, "applicantPage.html", {'applicant': applicant, 'applicantRoles': applicantRoles, 'rolesLeft': rolesLeft})
    
def rolePage(request, id):
    role = models.Role.objects.get(id=id)
    if not role:
        return redirect('home')
    applicantRoles = models.ApplicantRole.objects.filter(role=id).order_by('status')
    applicants = models.ApplicantRole.objects.filter(role=role).values_list('applicant', flat=True).distinct()
    applicantsLeft = models.Applicant.objects.exclude(id__in=applicants).count()
    return render(request, "rolePage.html", {'role': role, 'applicantRoles': applicantRoles, 'applicantsLeft': applicantsLeft})
    
    
def addApplicant(request):
    if request.method == "GET":
        return render(request, "newApplicant.html", {'roles': models.Role.objects.all(), 'status': [x[0] for x in models.ApplicantRole.Status.choices]}) 
    if request.method == "POST":
        name = request.POST['name']
        phoneNumber = request.POST['phoneNumber']
        email = request.POST['email']
        
        role1 = request.POST['role1']
        status1 = request.POST['status1']
        role2 = request.POST['role2']
        status2 = request.POST['status2']
        role3 = request.POST['role3']
        status3 = request.POST['status3']
        
        # Verify if applicant already exists by it's email or phone number
        applicant = models.Applicant.objects.filter(phoneNumber=phoneNumber)
        print(applicant)
        applicant2 = models.Applicant.objects.filter(email=email)
        print(applicant2)
        # If it exists, warn the user
        if applicant or applicant2:
            print("Error")
            return redirect('home')  
        
        # Else
        applicant = models.Applicant(name=name, phoneNumber=phoneNumber, email=email)
        applicant.save()
        
        # Check the roles
        if role1 != '---' and status1 != '---':
            role = models.ApplicantRole(role=models.Role.objects.get(id=role1), applicant=applicant, status=status1)
            role.save()
        if role2 != '---' and status2 != '---':
            role = models.ApplicantRole(role=models.Role.objects.get(id=role2), applicant=applicant, status=status2)
            role.save()
        if role3 != '---' and status3 != '---':
            role = models.ApplicantRole(role=models.Role.objects.get(id=role3), applicant=applicant, status=status3)
            role.save()
            
        return redirect('applicantPage', id=applicant.id)
        

    return redirect('home')    
    
    

def addRole(request):
    if request.method == "GET":
        return render(request, "newRole.html")  
    if request.method == "POST":
        name = request.POST['name']
        
        # Verify if it exists
        role = models.Role.objects.filter(name=name)
        if role:
            return redirect('home') 
        # Else
        role = models.Role(name=name)
        role.save()
        return render(request, "rolePage.html", {'role': role, 'applicantRoles': None})
        
    return redirect('home') 

def editApplicant(request, id):
    applicant = models.Applicant.objects.get(id=id)
    if applicant:
        applicantRoles = models.ApplicantRole.objects.filter(applicant=applicant)
        if request.method == "GET":
            return render(request, "editApplicant.html", {'applicant': applicant, 'applicantRoles': applicantRoles, 'roles': models.Role.objects.all(), 'status': [x[0] for x in models.ApplicantRole.Status.choices]}) 
        if request.method == "POST":
            name = request.POST['name']
            phoneNumber = request.POST['phoneNumber']
            email = request.POST['email']
            
            applicant.name = name
            applicant.phoneNumber = phoneNumber
            applicant.email = email
            applicant.save()
            
            for i in range(len(applicantRoles)):
                applicantRoles[i].status = request.POST['status' + str(applicantRoles[i].id)]
                applicantRoles[i].save()

            
            return redirect('applicantPage', id=id)
    return redirect('home')    

def deleteApplicant(request, id):
    applicant = models.Applicant.objects.get(id=id)
    applicant.delete()
    return redirect('home') 

def deleteRole(request, id):
    role = models.Role.objects.get(id=id)
    role.delete()
    return redirect('home') 


def addApplicantRole(request, id):
    applicant = models.Applicant.objects.get(id=id)
    if not applicant:
        return redirect('home') 
        
    # Get the roles the applicant already has
    applicantRoles = models.ApplicantRole.objects.filter(applicant=id).values_list('role', flat=True)
    # And get the ones left
    roles = models.Role.objects.exclude(id__in=applicantRoles)
    status = [x[0] for x in models.ApplicantRole.Status.choices]
    
    if request.method == "GET":
        return render(request, "addApplicantRole.html", {'applicant': applicant, 'roles': roles, 'status': status}) 
    if request.method == "POST":
        role = request.POST['role']
        stat = request.POST['status']
        
        if role == '---' or stat == '---':
            return render(request, "addApplicantRole.html", {'applicant': applicant, 'roles': roles, 'status': status}) 
        
        applicantRole = models.ApplicantRole(role=models.Role.objects.get(id=role), status=stat, applicant=applicant)             
        applicantRole.save()        
        return redirect('applicantPage', id=id)

def deleteApplicantRole(request, applicantId, roleId):
    applicant = models.Applicant.objects.get(id=applicantId)
    if not applicant:
        return redirect('home')
    applicantRole = models.ApplicantRole.objects.filter(applicant=applicantId, role=roleId)
    if applicantRole:
        applicantRole.delete()
        return redirect('editApplicant', id=applicantId)

def deleteRoleApplicant(request, roleId, applicantId):
    role = models.Role.objects.get(id=roleId)
    if not role:
        return redirect('home')
    applicantRole = models.ApplicantRole.objects.filter(applicant=applicantId, role=roleId)
    if applicantRole:
        applicantRole.delete()
        return redirect('rolePage', id=roleId)
    
def addRoleApplicant(request, id):
    role = models.Role.objects.get(id=id)
    if not role:
        return redirect('home')
    if request.method == "GET":
        applicants = models.ApplicantRole.objects.filter(role=role).values_list('applicant', flat=True).distinct()
        applicantsLeft = models.Applicant.objects.exclude(id__in=applicants)
        status = [x[0] for x in models.ApplicantRole.Status.choices]
        return render(request, "addRoleApplicant.html", {'role': role, 'applicantsLeft': applicantsLeft, 'status': status})
    if request.method == "POST":
        applicantId = request.POST['applicant']
        status = request.POST['status']
        applicant = models.Applicant.objects.get(id=applicantId)
        applicantRole = models.ApplicantRole(applicant=applicant, role=role, status=status)
        applicantRole.save()
        return redirect('rolePage', id=id)