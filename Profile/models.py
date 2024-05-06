from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.
STATUS_CHOICES = (
        ('process', 'In Process'),
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('onhold', 'On Hold'),
    )

GENDER_CHOICES = (
        (1, 'Male'),
        (0, 'Female'),
    )
    
class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(validators=[MinValueValidator(0)], default=0, null=True, blank=True)
    sex = models.IntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    link = models.SlugField(blank=True)

    def __str__(self):
        return self.user.username

    
    def get_absolute_url(self):
        return reverse("predict", kwargs={"slug": self.link})
    

    def save(self, *args, **kwargs):
        if not self.link and self.user:
            self.link = '-'.join((slugify(self.user.username),slugify(self.age)))
        return super(ProfileModel, self).save(*args, **kwargs)


class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
