from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class DetailJob(models.Model):
    jname=models.CharField(max_length=100)
    jdesc=models.TextField()
    company=models.CharField(max_length=200)
    location=models.CharField(max_length=200)
    salary=models.FloatField()
    experience=models.CharField(max_length=50)
    skills=models.TextField()

class DetailData(models.Model):
    applied=models.CharField(max_length=200)
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=50)
    contact=models.CharField(max_length=15)
    email=models.EmailField(max_length=100)
    edu=models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    address=models.TextField()    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    