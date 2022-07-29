from django.contrib import admin

from quizzes.models import Choice, Quiz

# Register your models here.
admin.site.register(Choice)
admin.site.register(Quiz)