from django.contrib import admin

from quizzes.models import Choice, Quiz, Question, QuizData, Score

# Register your models here.
admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(QuizData)
admin.site.register(Score)