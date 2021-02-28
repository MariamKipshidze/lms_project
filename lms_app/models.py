from django.db import models
from users.models import User

from django.utils.translation import gettext_lazy as _
from PIL import Image


class Faculty(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Faculty name"))


class Subject(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Subject name"))
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name=_("Faculty"))
    credit_score = models.SmallIntegerField(verbose_name=_("Credit Score"))
    lecturer = models.ManyToManyField(User, verbose_name=_("Lecturer"))


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Student"))
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, verbose_name=_("Faculty"), default=0)
    first_name = models.CharField(max_length=50, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    mobile_number = models.CharField(max_length=20, verbose_name=_("Mobile Number"), default="")
    personal_id = models.CharField(max_length=11, verbose_name=_("Personal ID"), default="")
    image = models.ImageField(default="default.jpg", upload_to="profile_pics", verbose_name=_("Profile Picture"))
    gpa = models.DecimalField(max_digits=3, decimal_places=2, verbose_name=_('GPA'))
    subject = models.ManyToManyField(Subject, verbose_name=_("Subject"), default=0)

    def __str__(self):
        return f"{self.user.email} {self.user.last_name} Profile"

    def save(self, *args, **kwargs):
        super(StudentProfile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class LecturerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Student"))
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, verbose_name=_("Faculty"))
    first_name = models.CharField(max_length=50, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    mobile_number = models.CharField(max_length=20, verbose_name=_("Mobile Number"))
    personal_id = models.CharField(max_length=11, verbose_name=_("Personal ID"))

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Profile"

