from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator
# Create your models here.

now = timezone.now()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year = models.CharField(max_length=250)
    course = models.CharField(max_length=50)
    def __str__(self):
        return self.user.username


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    def __str__(self):
        return self.user.username
    
class Materials(models.Model):
    name = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    profile_pic = models.FileField(upload_to='media/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],)
    borrowed_date = models.DateTimeField(default=now, blank=True, null=True)
    deadline = models.DateTimeField(default=now, blank=True, null=True)
    borrower = models.CharField(max_length=250, blank=True)
    borrower_year = models.CharField(max_length=250, blank=True)
    borrower_course = models.CharField(max_length=250, blank=True)
    
class Forum(models.Model):
    title = models.CharField(max_length=10000)
    file = models.FileField(
        upload_to='media/announcement',
        validators=[ 
            FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'pdf', 'word', 'ppt', 'xlsx', 'csv', 'gif'])
        ],
        null=True,  # Allow null values
        blank=True  # Also allow empty values (in forms)
    )
    upload_date = models.DateTimeField(default=now)
    description = models.TextField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)


class Comments(models.Model):
    post = models.ForeignKey(Forum, on_delete=models.CASCADE)
    commentors = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(default=now)