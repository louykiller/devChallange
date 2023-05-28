from django.db import models

# Create your models here.
class Applicant(models.Model):
    name = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    #avatar (optional)
    
    def __str__(self):
        return self.name + ', ' + self.phoneNumber + ', ' + self.email
    
class Role(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name    
    
class ApplicantRole(models.Model):
    class Status(models.TextChoices):
        APPROVED = "Approved"
        REJECTED = "Rejected"
        UNDER_ANALYSIS = "Under Analysis"
        
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.UNDER_ANALYSIS)
    
    class Meta:
        unique_together = ('role', 'applicant',)
    
    def __str__(self):
        return self.applicant.name + ' -> ' + self.role.name + ' == ' + self.status
