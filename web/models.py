from django.contrib.auth.models import Permission, User
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    prerequisite = models.BooleanField(default=False)
    credit = models.IntegerField()

    def __str__(self):
        return self.title


class Student(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    clas = models.CharField(max_length=200)
    faculty = models.CharField(max_length=200)
    major = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(0)])

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
