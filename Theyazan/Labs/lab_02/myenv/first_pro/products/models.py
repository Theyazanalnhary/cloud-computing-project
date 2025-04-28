from django.db import models

# Create your models here.

class products (models.Model):
      name= models.CharField(max_length=100)
      content= models.TextField()
      price= models.DecimalField(max_digits=5,decimal_places=3)
      image= models.ImageField(upload_to='photos/%y/%m/%d', null=True, blank=True)
      active= models.BooleanField(True)