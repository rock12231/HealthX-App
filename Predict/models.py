from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
# Create your models here.

CAT_CHOICES = (
        (1, 'Doctor'),
        (0, 'Patient'),
    )
class ChatModel(models.Model):
    user = models.CharField(max_length=100)
    type = models.IntegerField(choices=CAT_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    link = models.SlugField(blank=True)
    
    
    class Meta:
        ordering = ('timestamp',)
        
    def get_absolute_url(self):
        return reverse("predict", kwargs={"slug": self.link})
    

    def save(self, *args, **kwargs):
        if not self.link and self.user:
            self.link = (slugify(self.user.username))
        return super(ChatModel, self).save(*args, **kwargs)