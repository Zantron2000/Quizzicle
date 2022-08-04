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

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    points = models.PositiveSmallIntegerField(default=1)
    subject = models.CharField(max_length=2, choices=Subject.choices)
    specific_subject = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    taken = models.ManyToManyField(User, through="QuizData")

    @property
    def valid_questions(self):
        valid_questions: int = 0

        for question in self.question_set.all():
            if(question.answerable):
                valid_questions += 1

        return valid_questions

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)

    @property
    def answerable(self):
        for choice in self.choice_set.all():
            if(choice.correct):
                return True

        return False

class Choice(models.Model):
    choice = models.CharField(max_length=500)
    correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class QuizData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

class Score(models.Model):
    score = models.PositiveSmallIntegerField()
    time = models.DateTimeField(auto_now_add=True)
    takenQuiz = models.ForeignKey(QuizData, on_delete=models.CASCADE)
