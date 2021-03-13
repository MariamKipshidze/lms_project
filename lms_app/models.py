from django.db import models

from users.models import User
from lms_app.choices import Grades

from django.utils.translation import gettext_lazy as _
from PIL import Image


class Faculty(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Faculty name"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    description = models.TextField(verbose_name=_("Description"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')


class Subject(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Subject name"))
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name=_("Faculty"))
    syllabus = models.FileField(upload_to="files/syllabus", verbose_name=_('Syllabus'), blank=True, null=True)
    credit_score = models.SmallIntegerField(verbose_name=_("Credit Score"))
    score = models.SmallIntegerField(verbose_name=_("Score"), default=100)
    lecturer = models.ManyToManyField(User, verbose_name=_("Lecturer"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name=_("Student"),
                                related_name="student_profile")
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, verbose_name=_("Faculty"), related_name="student")
    first_name = models.CharField(max_length=50, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    mobile_number = models.CharField(max_length=20, verbose_name=_("Mobile Number"))
    personal_id = models.CharField(max_length=11, verbose_name=_("Personal ID"), unique=True)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics", verbose_name=_("Profile Picture"))
    gpa = models.DecimalField(max_digits=3, decimal_places=2, verbose_name=_('GPA'), default=0)

    def __str__(self):
        return f"{self.user.email} {self.user.last_name} Profile"

    def save(self, *args, **kwargs):
        super(StudentProfile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')


class ChosenSubject(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE,
                                verbose_name="Student",
                                related_name="subject")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_("Subject"))
    current_score = models.SmallIntegerField(verbose_name=_("Current Score"), default=0)
    passed = models.BooleanField(verbose_name=_('Passed'), default=False)
    grades = models.PositiveSmallIntegerField(choices=Grades.choices, default=6)

    def __str__(self):
        return self.subject.name

    class Meta:
        verbose_name = _('Chosen Subject')
        verbose_name_plural = _('Chosen Subjects')
        unique_together = ["student", "subject"]


class LecturerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name=_("Lecturer"),
                                related_name="lecturer_profile")
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, verbose_name=_("Faculty"))
    first_name = models.CharField(max_length=50, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    mobile_number = models.CharField(max_length=20, verbose_name=_("Mobile Number"))
    personal_id = models.CharField(max_length=11, verbose_name=_("Personal ID"))
    salary = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Salary'))

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Profile"

    class Meta:
        verbose_name = _('Lecturer')
        verbose_name_plural = _('Lecturers')
