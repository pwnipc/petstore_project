from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Pet(models.Model):
    image = CloudinaryField('image')
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name