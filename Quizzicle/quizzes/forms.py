from django import forms
from django.db import models

from quizzes.models import Quiz, Question, Choice

class NewQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'points', 'subject', 'specific_subject']

    def __init__(self, *args, **kwargs):
        super(NewQuizForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'
            visible.field.widget.attrs['id'] = visible.name

class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']
    
    def __init__(self, *args, **kwargs):
        super(NewQuestionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'
            visible.field.widget.attrs['id'] = visible.name

class NewChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice', 'correct']

    def __init__(self, *args, **kwargs):
        super(NewChoiceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'
            visible.field.widget.attrs['id'] = visible.name

class SearchForm(forms.Form):
    class SubjectChoices(models.TextChoices):
        NONE = "NA"
        MATH = "MA"
        SCIENCE = "SC"
        HISTORY = "HI"
        ENGLISH = "EN"
        MISC = "MC"

    name = forms.CharField(max_length=50, required=False)
    subject = forms.ChoiceField(choices=SubjectChoices.choices, required=False)
    specific_subject = forms.CharField(max_length=50, required=False)
    author = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'
            visible.field.widget.attrs['id'] = visible.name

