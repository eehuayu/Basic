from django.db import models
from datetime import datetime
import uuid

from django.utils import timezone

class Employee(models.Model):
    employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    user_name = models.CharField(max_length=30)
    pwd = models.CharField(max_length=50)
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    entry_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user_name

class Base(models.Model):
    entry_date = models.DateTimeField(auto_now=True) 
    entry_user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s", null=True)
    
    class Meta:
        abstract = True        

class EmployeeIP(Base):
    IP = models.GenericIPAddressField(max_length=30, unique=True, primary_key=True)  
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.IP

class Punch(Base):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    punch_date = models.DateTimeField(default=timezone.now)
    is_normal = models.BooleanField(default=True)
    IP = models.GenericIPAddressField(max_length=30)

class Adjustment(Base):
    ADJUSTMENT_TYPES = (
        ('L', 'Leave'),
        ('O', 'Over Time'),
    )    

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

class AdjustmentLog(Base):
    ADJUSTMENT_OPERATIONS = (
        ('1', 'Approved'),
        ('2', 'Denied'),
    )

    leave = models.ForeignKey(Adjustment, on_delete=models.CASCADE)
    operation = models.CharField(max_length=10, choices=ADJUSTMENT_OPERATIONS)

class Test(models.Model):
    msg = models.CharField(max_length=500)
    item = models.CharField(max_length=100, null=True)
    entry_date = models.DateTimeField(auto_now=True)