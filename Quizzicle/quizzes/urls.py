from django.urls import path

from quizzes import views

urlpatterns = [
    path("", views.view_created_quizzes, name="view_quizzes"),
    path("create_quiz/", views.create_quiz, name="create_quiz"),
    path("modify_quiz/<int:id>/", views.modify_quiz, name="modify_quiz"),
    path("delete_quiz/<int:id>/", views.delete_quiz, name="delete_quiz"),
    path("delete_question/<int:id>", views.delete_question, name="delete_question"),
    path("create_question/<int:id>", views.create_question, name="create_question"),
    path("modify_question/<int:id>/", views.modify_question, name="modify_question"),
    path("create_choice/<int:id>/", views.create_choice, name="create_choice"),

    path("update_choice/<int:id>", views.modify_choice, name="modify_choice")
]