from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    ID = models.CharField(max_length=10, primary_key=True) # id
    course_name = models.CharField(max_length=100) # name
    course_lecturer = models.CharField(max_length=100) # lecturer
    course_des = models.CharField(max_length=250) # description
    course_semester = models.CharField(max_length=1, default='1') # semester
    course_year = models.CharField(max_length=4, default="2566") # year
    course_seat = models.IntegerField(default=40) # seat
    course_status = models.BooleanField(default=True) # status

    def __str__(self):
        return f'{self.ID} : {self.course_name} Seat :{self.course_seat}' 
    


class Register(models.Model):
    reg_scholar_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reg_course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.reg_scholar_id} : {self.reg_course_id}'