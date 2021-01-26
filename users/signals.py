from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from .models import StudentProfile

@receiver(post_save, sender =  User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user  = instance)


@receiver(post_save, sender =  User)
def save_profile(sender, instance,  **kwargs):
    instance.studentprofile.save()