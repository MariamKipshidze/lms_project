from django.db.models import IntegerChoices


class Grades(IntegerChoices):
    A = 1,
    B = 2,
    C = 3,
    D = 4,
    E = 5,
    F = 6,
