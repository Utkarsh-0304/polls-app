import strawberry
import strawberry_django
from typing import Optional
from strawberry_django.optimizer import DjangoOptimizerExtension


from .types import Question, Choice, QuestionInput, QuestionInputPartial
from . import models

@strawberry.type
class Query:
    
    @strawberry_django.field()
    def questions(self, question_text: Optional[str] = None) -> list[Question]:

        qs = models.Question.objects.all()

        if question_text: 
            qs = qs.filter(question_text__icontains=question_text)
        
        return qs
        
    choices: list[Choice] = strawberry_django.field()

@strawberry.type
class Mutation:
    create_question: Question = strawberry_django.mutations.create(
        QuestionInput,
        handle_django_errors=True
    )

    delete_question: Question = strawberry_django.mutations.delete(
        QuestionInputPartial,
        handle_django_errors=True
    )

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension
    ]
)