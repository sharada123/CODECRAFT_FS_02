from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role_choices = (('admin', 'admin'),('employee', 'employee'),)
    role = models.CharField(max_length=8, choices=role_choices,default='employee')
    confirm_password = models.CharField(max_length=10, default="confirm")
    def __str__(self):
        return self.username
class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_joining = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    def __str__(self):
        return self.first_name + ' ' + self.last_name