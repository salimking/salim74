from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Input(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    input_values = models.TextField()
    search_value = models.IntegerField()
    output = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
