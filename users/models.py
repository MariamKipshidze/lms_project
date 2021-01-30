from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .choices import StatusChoices
from PIL import Image


class User(AbstractUser):
    status = models.PositiveSmallIntegerField(_("Status"), choices=StatusChoices.choices, default=StatusChoices.Other)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = _("Student"))
    image = models.ImageField(default = "default.jpg", upload_to = "profile_pics", verbose_name = _("Profile Picture"))

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super(StudentProfile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


