from email.headerregistry import Address
from django.db import models

#from Handler.views import Categories



class SignUp_info(models.Model):
    Full_Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Password = models.CharField(max_length=100)
    Contact = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Email

class Books(models.Model):
    User = models.IntegerField()
    Category = models.CharField(max_length=100)
    Name = models.CharField(max_length=100)
    Rate = models.CharField(max_length=100)
    About = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Name 

class Cookie_Handler(models.Model):
    Cookie = models.CharField(max_length=100)
    User = models.IntegerField()
    Type = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Cookie  