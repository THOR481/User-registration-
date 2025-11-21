from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, null=True, blank=True)   # OTP column
    verified=models.BooleanField(default=False)
    otp_created_at = models.DateTimeField(null=True, blank=True)  # Optional

    def __str__(self):
        return self.user.username
