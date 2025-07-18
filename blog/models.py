from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.

class Blog(models.Model):
    MY_CHOICES = (
        (1, '😞 1 - Nagyon rossz'),
        (2, '😒 2 - Rossz'),
        (3, '😐 3 - Elmegy'),
        (4, '🙂 4 - Jó'),
        (5, '😍 5 - Tökéletes'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)                 
    content = models.TextField()                            
    timestamp = models.DateTimeField(auto_now_add=True)   
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    my_choice_rating = models.IntegerField(choices=MY_CHOICES, default=3)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title
    
class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title