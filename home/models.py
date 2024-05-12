from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.exceptions import ValidationError

from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUser(AbstractUser):
    user_id=models.CharField(max_length=100, default="userid",primary_key=True,unique=True)

    def __str__(self):
        return  f"{self.username} - {self.user_id}"   

   



class Course(models.Model):
    course_id = models.CharField(max_length=20, unique=True, default="courseid", primary_key=True)
    course_name = models.CharField(max_length=50, default="coursename")
    category = models.CharField(max_length=20, default="category")
    course_description = models.CharField(max_length=250)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course_price = models.IntegerField(
        validators=[
            MinValueValidator(500, message='Course price must be at least 500.'),
            MaxValueValidator(2000, message='Course price cannot exceed 2000.'),
        ]
    )
    course_image= models.ImageField(upload_to='images/',blank=True,null=True)
    course_content = models.FileField(upload_to='files/', blank=True, null=True)
    course_topic1=models.CharField(max_length=100,default="coursename")
    course_topic2=models.CharField(max_length=100,default="coursename")
    course_topic3=models.CharField(max_length=100,default="coursename")
    course_topic4=models.CharField(max_length=100,default="coursename")


    def save(self, *args, **kwargs):
        # Generate a unique course_id using UUID if not provided
        if not self.course_id or self.course_id == "courseid":
            self.course_id = "course" + str(uuid.uuid4().hex[:6])
        super().save(*args, **kwargs)

 
    def __str__(self):
        return  f"{self.course_name} - {self.course_id}"
    

class CartItem(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return  f"{self.user_id.username} - {self.course_id.course_name}"   
    
class Payment(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return  f"{self.user_id.username} - {self.course_id.course_name}"  
    

    

class Question(models.Model):
    question_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_text = models.TextField(blank=True, null=True)
    is_answered = models.BooleanField(default=False)
    course_id=models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student_id} "
    
class Feedback(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='instructor_feedbacks')
    feedback_text = models.TextField()


    def __str__(self):
        return f"{self.student} -> {self.course.instructor} -> {self.course.course_name} "
    
