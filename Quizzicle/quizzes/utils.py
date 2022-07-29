from quizzes.models import Quiz, Question, Choice

def get_quiz(id: int):
    try:
        return Quiz.objects.get(id=id)
    except:
        return None

def get_question(id: int):
    try:
        return Question.objects.get(id=id)
    except:
        return None

def get_choice(id: int):
    try:
        return Choice.objects.get(id=id)
    except:
        return None