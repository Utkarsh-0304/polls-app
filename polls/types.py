import strawberry_django
from strawberry import auto

from . import models

@strawberry_django.type(models.Choice)
class Choice:
    id: auto
    question: "Question"
    choice_text: auto
    votes: auto


@strawberry_django.type(models.Question)
class Question:
    id: auto
    question_text: auto
    pub_date: auto
    choice_set: list[Choice]

@strawberry_django.input(models.Question)
class QuestionInput:
    question_text: auto
    pub_date: auto

@strawberry_django.partial(models.Question)
class QuestionInputPartial:
    id: auto
    question_text: auto
    pub_date: auto