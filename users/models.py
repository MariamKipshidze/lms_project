from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .choices import StatusChoices


class User(AbstractUser):
    status = models.PositiveSmallIntegerField(_("Status"), choices=StatusChoices.choices, default=StatusChoices.Other)
