from django.db.models import IntegerChoices


class Grades(IntegerChoices):
    A = 5,
    B = 4,
    C = 3,
    D = 2,
    E = 1,
    F = 0,
