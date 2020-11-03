from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class userdata(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField(max_length=100)
    message = models.CharField(max_length = 2000)

    def __str__(self):
        return self.name + '-' + self.subject

class workshop(models.Model):
    topic = models.CharField(max_length=100)
    date = models.DateField()
    desc = models.CharField(max_length= 160)

    def __str__(self):
        return self.topic + '-' + str(self.date)