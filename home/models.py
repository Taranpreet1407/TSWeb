from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, datetime
class FullUserData(models.Model):
    email = models.EmailField(max_length = 100, primary_key = True)
    password = models.CharField(max_length = 100)
    full_name = models.CharField(max_length = 100)
    dob = models.DateField()
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    college = models.CharField(max_length = 100)
    experience = models.CharField(max_length = 30)
    passout = models.IntegerField(default = datetime.today().year)
    relocation = models.CharField(max_length = 30)
    find_us = models.CharField(max_length = 50)
    ref_id = models.CharField(max_length = 50, null = True)
    mobile_no = models.CharField(null = True, max_length = 12)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    resume_link = models.CharField(max_length = 512)
    payment = models.CharField(max_length = 3, default = 'No')
    option = models.IntegerField(default = 4)
    def __str__(self):
        return str(self.full_name)

class InternData(models.Model):
    intern_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(FullUserData, on_delete = models.CASCADE)
    target = models.IntegerField(default = 132)

    def __str__(self):
        return str(self.intern_id)

class WorkData(models.Model):
    intern_id = models.IntegerField(null = True)
    date = models.DateField(default = date.today)
    out_enrolled = models.IntegerField(default = 1)

    def __str__(self):
        return str(self.out_enrolled)


class Payments(models.Model):
    intern_id = models.ForeignKey(InternData, primary_key= True, on_delete = models.CASCADE)
    payment_id = models.CharField(max_length = 254)
    order_id = models.CharField(max_length = 254)
    signature = models.CharField(max_length = 254)

    def __str__(self):
        return str(self.intern_id)
    