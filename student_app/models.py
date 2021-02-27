from django.db import models
from users.models import User

from django.utils.translation import gettext_lazy as _
from PIL import Image


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Student"))
    first_name = models.CharField(max_length=50, verbose_name=_("First Name"), default="")
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"), default="")
    image = models.ImageField(default="default.jpg", upload_to="profile_pics", verbose_name=_("Profile Picture"))
    gpa = models.DecimalField(max_digits=3, decimal_places=2, verbose_name=_('GPA'), default=0)

    def __str__(self):
        return f"{self.user.email} Profile"

    def save(self, *args, **kwargs):
        super(StudentProfile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
