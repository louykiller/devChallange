from django.shortcuts import redirect, render
from . import models
from django.contrib import messages

# Create your views here.

def start(request):
    return render(request, "start.html")
    
def home(request):
    # Get all applicants and roles
    applicants = models.Applicant.objects.all().order_by('name')
    roles = models.Role.objects.all().order_by('name')
    # For each applicant get their roles
    applicantsRoles = []
    for applicant in applicants:
        applicantsRoles.append(models.ApplicantRole.objects.filter(applicant__exact=applicant.id))  
    # Save the data from every applicant
    applicantsData = None  
    if applicants:
        applicantsData = zip(applicants, applicantsRoles) 
    # For each role get their applicants
    rolesApplicants = []
    for role in roles:
        rolesApplicants.append(models.ApplicantRole.objects.filter(role__exact=role.id).order_by('status'))
    rolesData = None
    # Save the data from every role
    if roles:
        rolesData = zip(roles, rolesApplicants)
    # Render the index.html page with the data fetched
    return render(request, "index.html", {'applicantsData': applicantsData, 'rolesData': rolesData})


def search(request):
    if request.method == "POST":
        search = request.POST['search']
        # Get all applicants where the fields contain the search
        applicantNames = models.Applicant.objects.filter(name__icontains=search)
        applicantPhones = models.Applicant.objects.filter(phoneNumber__icontains=search)
        applicantEmails = models.Applicant.objects.filter(email__icontains=search)
        # Join them and sort by name
        applicants = sorted(applicantNames.union(applicantPhones.union(applicantEmails)),
                           key=lambda applicant: applicant.name)
        # For each applicant get their roles
        applicantsRoles = []
        for applicant in applicants:
            applicantsRoles.append(models.ApplicantRole.objects.filter(applicant__exact=applicant.id))  
        # Save the data from every applicant
        applicantsData = None  
        if applicants:
            applicantsData = zip(applicants, applicantsRoles) 
        # Get all applicants where the fields contain the search
        roles = models.Role.objects.filter(name__icontains=search).order_by('name')
        # For each role get their applicants
        rolesApplicants = []
        for role in roles:
            rolesApplicants.append(models.ApplicantRole.objects.filter(role__exact=role.id).order_by('status'))
        rolesData = None
        # Save the data from every role
        if roles:
            rolesData = zip(roles, rolesApplicants)
        messages.success(request, "Found " + str(len(applicants)) + " applicants and " + str(len(roles)) + " roles that match the search!")
        # Render the index.html page with the data fetched
        return render(request, "index.html", {'applicantsData': applicantsData, 'rolesData': rolesData})
    return redirect('home')
    

def applicantPage(request, id):
    # Get the applicant from it's id
    applicant = models.Applicant.objects.get(id=id)
    # If it doesn't exist redirect to home
    if not applicant:
        return redirect('home')
    # Get it's roles and roles left
    applicantRoles = models.ApplicantRole.objects.filter(applicant=id).order_by('role__name')
    rolesLeft = models.Role.objects.exclude(id__in=applicantRoles.values_list('role', flat=True)).count()
    # Render the applicant page with all the data fetched
    return render(request, "applicantPage.html", {'applicant': applicant, 'applicantRoles': applicantRoles, 'rolesLeft': rolesLeft})
    
def rolePage(request, id):
    # Get the role from it's id
    role = models.Role.objects.get(id=id)
    # If it doesn't exist redirect to home
    if not role:
        return redirect('home')
    # Get it's applicants with their status and the applicants left
    applicantRoles = models.ApplicantRole.objects.filter(role=id).order_by('applicant__name')
    applicants = models.ApplicantRole.objects.filter(role=role).values_list('applicant', flat=True).distinct()
    applicantsLeft = models.Applicant.objects.exclude(id__in=applicants).count()
    # Render the role page with all the data fetched
    return render(request, "rolePage.html", {'role': role, 'applicantRoles': applicantRoles, 'applicantsLeft': applicantsLeft})
    
    
def addApplicant(request):
    # If it's a GET request, load the new applicant page with the form
    if request.method == "GET":
        return render(request, "newApplicant.html", {'roles': models.Role.objects.all().order_by('name'), 'status': [x[0] for x in models.ApplicantRole.Status.choices]}) 
    # If it's a POST request
    if request.method == "POST":
        # Get all the info from the forms
        name = request.POST['name']
        phoneNumber = request.POST['phoneNumber']
        email = request.POST['email']
        # Verify if applicant already exists by it's email or phone number
        applicantPhone = models.Applicant.objects.filter(phoneNumber=phoneNumber)
        applicantEmail = models.Applicant.objects.filter(email=email)
        # If it exists, warn the user
        if applicantPhone:
            messages.error(request, "Phone Number already in use. Please try another one")
            return redirect('addApplicant')
        if applicantEmail:
            messages.error(request, "Email already in use. Please try another one")
            return redirect('addApplicant')
        # Save the new applicant
        applicant = models.Applicant(name=name, phoneNumber=phoneNumber, email=email)
        applicant.save()
        # Get all the roles
        role1 = request.POST['role1']
        status1 = request.POST['status1']
        role2 = request.POST['role2']
        status2 = request.POST['status2']
        role3 = request.POST['role3']
        status3 = request.POST['status3']
        # Check the roles (with try, except blocks because of UNIQUE constraint)
        try:
            if role1 != '---' and status1 != '---':
                role = models.ApplicantRole(role=models.Role.objects.get(id=role1), applicant=applicant, status=status1)
                role.save()
        except:
            print("Duplicate")
        try:
            if role2 != '---' and status2 != '---':
                role = models.ApplicantRole(role=models.Role.objects.get(id=role2), applicant=applicant, status=status2)
                role.save()
        except:
            print("Duplicate")
        try:
            if role3 != '---' and status3 != '---':
                role = models.ApplicantRole(role=models.Role.objects.get(id=role3), applicant=applicant, status=status3)
                role.save()
        except:
            print("Duplicate")
        messages.success(request, "Successfuly created applicant '" + name + "'")
        # Load the new applicant's page
        return redirect('applicantPage', id=applicant.id)
    return redirect('home')    
    

def addRole(request):
    # If it's a GET request, load the add role page with the form
    if request.method == "GET":
        return render(request, "newRole.html")  
    # If it's a POST request
    if request.method == "POST":
        # Get the role name
        name = request.POST['name']     
        # Verify if it exists
        role = models.Role.objects.filter(name__iexact=name)
        if role:
            messages.error(request, "Role name already exists. Please try another one")
            return redirect('addRole') 
        # Save the new role
        role = models.Role(name=name)
        role.save()
        # Load the new role's page
        messages.success(request, "Successfuly created the role '" + name + "'")
        return render(request, "rolePage.html", {'role': role, 'applicantRoles': None})
    return redirect('home') 

def editApplicant(request, id):
    # Check if the applicant exists
    applicant = models.Applicant.objects.get(id=id)
    if applicant:
        # Get it's roles
        applicantRoles = models.ApplicantRole.objects.filter(applicant=applicant)
        # If it's a GET request, load the edit applicant page with the form and respective data
        if request.method == "GET":
            return render(request, "editApplicant.html", {'applicant': applicant, 'applicantRoles': applicantRoles, 'roles': models.Role.objects.all().order_by('name'), 'status': [x[0] for x in models.ApplicantRole.Status.choices]}) 
        # If it's a POST request
        if request.method == "POST":
            # Get all the info from the forms
            name = request.POST['name']
            phoneNumber = request.POST['phoneNumber']
            email = request.POST['email']
             # Verify if applicant already exists by it's email or phone number
            applicantPhone = models.Applicant.objects.filter(phoneNumber=phoneNumber).exclude(id=id)
            applicantEmail = models.Applicant.objects.filter(email=email).exclude(id=id)
            # If it exists, warn the user
            if applicantPhone:
                messages.error(request, "Phone Number already in use. Please try another one")
                return redirect('editApplicant', id=id)
            if applicantEmail:
                messages.error(request, "Email already in use. Please try another one")
                return redirect('editApplicant', id=id)
            # Update the applicant's info
            applicant.name = name
            applicant.phoneNumber = phoneNumber
            applicant.email = email
            applicant.save()
            # Update it's roles status
            for i in range(len(applicantRoles)):
                applicantRoles[i].status = request.POST['status' + str(applicantRoles[i].id)]
                applicantRoles[i].save()
            # Redirect to the applicant page
            messages.success(request, "Successfuly updated applicant '" + name + "'")
            return redirect('applicantPage', id=id)
    messages.error(request, "Applicant not found")
    return redirect('home')    

def deleteApplicant(request, id):
    # Delete the applicant and redirect to the home page
    applicant = models.Applicant.objects.get(id=id)
    messages.success(request, "Deleted applicant '" + applicant.name + "'")
    applicant.delete()
    return redirect('home') 

def deleteRole(request, id):
    # Delete the role and redirect to the home page
    role = models.Role.objects.get(id=id)
    messages.success(request, "Deleted role '" + role.name + "'")
    role.delete()
    return redirect('home') 

def addApplicantRole(request, id):
    # Check if the applicant exists
    applicant = models.Applicant.objects.get(id=id)
    if not applicant:
        messages.success(request, "Applicant not found") 
        return redirect('home') 
    # Get the roles that the applicant already has
    applicantRoles = models.ApplicantRole.objects.filter(applicant=id).values_list('role', flat=True)
    # And get the ones left
    roles = models.Role.objects.exclude(id__in=applicantRoles)
    # Get the status values
    status = [x[0] for x in models.ApplicantRole.Status.choices]
    # If it's a GET request, load the add applicant role page with the form and respective data
    if request.method == "GET":
        return render(request, "addApplicantRole.html", {'applicant': applicant, 'roles': roles, 'status': status}) 
    # If it's a POST request
    if request.method == "POST":
        # Get the data from the form
        role = request.POST['role']
        stat = request.POST['status']
        # Check if it's valid
        if role == '---' or stat == '---':
            messages.warning(request, "Please select a valid option for both 'Role' and 'Status'")
            return redirect('addApplicantRole', id=id)
        # Create the new applicant role
        applicantRole = models.ApplicantRole(role=models.Role.objects.get(id=role), status=stat, applicant=applicant)             
        applicantRole.save()      
        # Redirect tho the applicant page  
        messages.success(request, "Successfuly added the role '" + applicantRole.role.name + "' to the applicant '" + applicantRole.applicant.name + "'")
        return redirect('applicantPage', id=id)

def deleteApplicantRole(request, applicantId, roleId):
    # Check if the applicant exists
    applicant = models.Applicant.objects.get(id=applicantId)
    if not applicant:
        messages.success(request, "Applicant not found")
        return redirect('home')
    # Check if the applicant role exists
    applicantRole = models.ApplicantRole.objects.filter(applicant=applicantId, role=roleId).first()
    # If it exists delete it and go to the edit applicant page
    if applicantRole:
        messages.success(request, "Deleted the role '" + applicantRole.role.name + "' from the applicant '" + applicantRole.applicant.name + "'")
        applicantRole.delete()
        return redirect('editApplicant', id=applicantId)
    messages.success(request, "This applicant does not have that role")
    return redirect('applicantPage', id=applicantId)
    
def addRoleApplicant(request, id):
    # Check if the role exists
    role = models.Role.objects.get(id=id)
    if not role:
        messages.success(request, "Role not found")
        return redirect('home')
    # If it's a GET request, load the add role applicant page with the form and respective data
    if request.method == "GET":
        # Get the applicants in this role
        applicants = models.ApplicantRole.objects.filter(role=role).values_list('applicant', flat=True).distinct()
        # And the ones left
        applicantsLeft = models.Applicant.objects.exclude(id__in=applicants)
        # Get the status values
        status = [x[0] for x in models.ApplicantRole.Status.choices]
        return render(request, "addRoleApplicant.html", {'role': role, 'applicantsLeft': applicantsLeft, 'status': status})
    # If it's a POST request
    if request.method == "POST":
        # Get the data from the form
        applicantId = request.POST['applicant']
        stat = request.POST['status']
        # Check if it's valid
        if applicantId == '---' or stat == '---':
            messages.warning(request, "Please select a valid option for both 'Applicant' and 'Status'")
            return redirect('addRoleApplicant', id=id)
        # Get the applicant
        applicant = models.Applicant.objects.get(id=applicantId)
        # Create the new applicant role
        applicantRole = models.ApplicantRole(applicant=applicant, role=role, status=stat)
        applicantRole.save()
        # Redirect tho the role page  
        messages.success(request, "Successfuly added the applicant '" + applicantRole.applicant.name + "' to the role '" + applicantRole.role.name + "'")
        return redirect('rolePage', id=id)
    
def deleteRoleApplicant(request, roleId, applicantId):
    # Check if the role exists
    role = models.Role.objects.get(id=roleId)
    if not role:
        messages.error(request, "No Role Found!")
        return redirect('home')
    # Check if the applicant role exists
    applicantRole = models.ApplicantRole.objects.filter(applicant=applicantId, role=roleId).first()
    # If it exists delete it and go to the role applicant page
    if applicantRole:
        messages.success(request, "Deleted the applicant '" + applicantRole.applicant.name + "' from the role '" + applicantRole.role.name + "'")
        applicantRole.delete()
        return redirect('rolePage', id=roleId)
    
def editRole(request, applicantId, roleId):
    # Check if the applicant exists
    applicant = models.Applicant.objects.get(id=applicantId)
    if not applicant:
        messages.success(request, "Applicant not found")
        return redirect('home')
    # Check if the applicant role exists
    applicantRole = models.ApplicantRole.objects.filter(applicant=applicantId, role=roleId).first()
    # If it exists 
    if applicantRole:
        if request.method == "GET":
            # Get the status values
            status = [x[0] for x in models.ApplicantRole.Status.choices]
            status.remove(applicantRole.status)
            return render(request, 'editRole.html', {'applicantRole': applicantRole, 'status': status})
        if request.method == "POST":
            status = request.POST['status']
            applicantRole.status = status
            messages.success(request, "Successfuly updated the status of the applicant '" + applicantRole.applicant.name + "' for the role '" + applicantRole.role.name + "' to '" + status + "'")
            applicantRole.save() 
    else:
        messages.success(request, "This applicant does not have that role ")
    return redirect('rolePage', id=roleId)
