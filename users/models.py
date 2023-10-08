from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Scholar(models.Model):
    ID = models.OneToOneField(User, on_delete=models.CASCADE) # id
    scholar_name = models.CharField(max_length=100) # name
    scholar_email = models.CharField(max_length=100) # email

    def __str__(self):
        return f'{self.ID} + " : " + {self.scholar_name}'
    
    def get_id(self):
        return f'{self.ID}'
    
    def get_name(self):
        return f'{self.scholar_name}'
    
    def get_email(self):
        return f'{self.scholar_email}'