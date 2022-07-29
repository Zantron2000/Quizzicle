from django.urls import path

from quizzes import views

urlpatterns = [
    path("create/view_quizzes", views.view_created_quizzes, name="view_quizzes"),
    path("create/create_quiz/", views.create_quiz, name="create_quiz"),
    path("create/modify_quiz/<int:id>/", views.modify_quiz, name="modify_quiz"),
    path("create/delete_quiz/<int:id>/", views.delete_quiz, name="delete_quiz"),
    path("create/delete_question/<int:id>", views.delete_question, name="delete_question"),
    path("create/create_question/<int:id>", views.create_question, name="create_question"),
    path("create/modify_question/<int:id>/", views.modify_question, name="modify_question"),

    path("create/update_choice/<int:id>", views.modify_choice, name="modify_choice")
]