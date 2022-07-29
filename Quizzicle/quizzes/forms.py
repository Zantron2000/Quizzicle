from django import forms

from quizzes.models import Quiz, Question, Choice

class NewQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['points', 'subject', 'specific_subject', 'name']

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
        super(NewQuizForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'
            visible.field.widget.attrs['id'] = visible.name

class NewChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice', 'correct']

    def __init__(self, *args, **kwargs):
        super(NewQuizForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'
            visible.field.widget.attrs['id'] = visible.name