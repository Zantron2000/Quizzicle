from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Quiz(models.Model):
    class Subject(models.TextChoices):
        MATH = "MA"
        SCIENCE = "SC"
        HISTORY = "HI"
        ENGLISH = "EN"
        MISC = "MC"

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField(default=1)
    subject = models.CharField(max_length=2, choices=Subject.choices)
    specific_subject = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)

class Choice(models.Model):
    choice = models.CharField(max_length=500)
    correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)