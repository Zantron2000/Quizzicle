from quizzes.models import Quiz, Question, Choice, QuizData, Score

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

def get_quiz_data(user, quiz):
    try:
        return QuizData.objects.get(user=user, quiz=quiz)
    except:
        return None

def process_test(quiz: Quiz, quiz_data):
    num_correct = 0

    for key in quiz_data:
        if(key == "csrfmiddlewaretoken"):
            continue

        question: Question = get_question(int(key))
        if(question is not None and question.answerable):

            answer: Choice = get_choice(quiz_data[key])
            if(answer in question.choice_set.all() and answer.correct):
                num_correct += 1

    return round(num_correct / quiz.valid_questions * 100)

