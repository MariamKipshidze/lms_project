from django.db.models import IntegerChoices


class StatusChoices(IntegerChoices):
    Teacher = 1
    Student = 2
    Other = 3