from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role_choices = (('admin', 'admin'),('employee', 'employee'),)
    role = models.CharField(max_length=8, choices=role_choices,default='employee')
    confirm_password = models.CharField(max_length=10, default="confirm")
    def __str__(self):
        return self.username


class Employee(models.Model):
    first_name = models.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[A-Za-z]+$', 'First name should only contain letters.')]
    )
    last_name = models.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[A-Za-z]+$', 'Last name should only contain letters.')]
    )
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50,validators=[RegexValidator(r'^[A-Za-z]+$', 'Department should only contain letters.')])
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0, 'Salary must be a positive number.')]
    )
    date_of_joining = models.DateField(auto_now_add=True)
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^[6-9]\d{9}$', 'Enter a valid phone number.')]
    )

    def clean(self):
        """Custom validation logic"""
        if self.first_name and len(self.first_name) < 2:
            raise ValidationError({'first_name': 'First name must be at least 2 characters long.'})

        if self.last_name and len(self.last_name) < 2:
            raise ValidationError({'last_name': 'Last name must be at least 2 characters long.'})

        if self.salary and self.salary < 0:
            raise ValidationError({'salary': 'Salary cannot be negative.'})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
