from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    birth=models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Job(models.Model):
    name=models.CharField(max_length=100)
    desc=models.TextField()
    users=models.ForeignKey(User, related_name="post",on_delete=models.CASCADE,blank=True, null=True)
    job_owner = models.ForeignKey(User, related_name="my_jobs", null=True, blank=True, on_delete=models.CASCADE)
    location=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

# class Myjob(models.Model):  
#     own=models.ForeignKey(Job, related_name="own",on_delete=models.CASCADE)
#     user=models.ForeignKey(User, related_name="my_user",on_delete=models.CASCADE,blank=True, null=True)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
