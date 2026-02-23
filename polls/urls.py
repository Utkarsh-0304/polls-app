from django.urls import path
from django.contrib.auth.decorators import login_required


from . import views

app_name="polls"
urlpatterns = [   
    path("", login_required(views.IndexView.as_view()), name="index"),
    path("<int:pk>/", login_required(views.DetailView.as_view()), name="detail"),
    path("<int:pk>/results/", login_required(views.ResultsView.as_view()), name="results"),
    path("<int:question_id>/vote/", login_required(views.vote), name="vote"),
    path("create_poll/", login_required(views.create_poll), name="create_poll"),
    path("delete_poll/<int:question_id>", login_required(views.delete_poll), name="delete_poll"),
    path("user/<str:username>", login_required(views.user_page), name="user_page")
]