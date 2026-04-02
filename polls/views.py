from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages


from .models import Question, Choice, Comment


@method_decorator(never_cache, name='dispatch')
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voted_polls = self.request.session.get('voted_polls', {})
        
        context['selected_choice'] = voted_polls.get(str(self.object.id))
        
        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_comments = self.object.comment_set.all().order_by('-created_at')
        
        # Get user's comments and others' comments separately
        user_comments = all_comments.filter(creator=self.request.user)
        other_comments = all_comments.exclude(creator=self.request.user)
        
        # Combine them: User first, then the rest
        context['sorted_comments'] = list(user_comments) + list(other_comments)
        return context


def vote(request, question_id):

    voted_polls = request.session.get('voted_polls', {})
    if question_id in voted_polls:
        messages.error(request, "You have already voted on this poll.")
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        voted_polls[question.id] = selected_choice.id
        request.session['voted_polls'] = voted_polls
        request.session.modified = True

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
def create_poll(request):

    if request.method == "POST":

        question_text = request.POST.get('question_text')
        q = Question.objects.create(
            question_text=question_text,
            pub_date=timezone.now(),
            user=request.user
        )

        choice_list = request.POST.getlist('choice')

        for text in choice_list:
            if text.strip():
                Choice.objects.create(
                    choice_text=text,
                    question=q
                )
        
        return render(request, "polls/create_poll.html", {"success_message": "Poll created successfully"})

    return render(request, "polls/create_poll.html", {'previous_url': request.META.get('HTTP_REFERER')})

def user_page(request, username):
    return render(request, "polls/user_page.html", {"user_polls": Question.objects.filter(user=request.user).order_by("-pub_date")})

def delete_poll(request, question_id):

    if request.method == "POST":
        q = get_object_or_404(Question, id=question_id)

        if q.user == request.user:
            q.delete()

        return redirect("polls:user_page", username=request.user.username)

    return redirect("polls:user_page", username=request.user.username)

def create_comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method != "POST":
        return redirect("polls:results", pk=question.id)

    comment_text = (request.POST.get("comment_text") or "").strip()
    if not comment_text:
        messages.error(request, "Comment cannot be empty.")
        return redirect("polls:results", pk=question.id)

    Comment.objects.create(
        text=comment_text,
        creator=request.user,
        created_at=timezone.now(),
        question=question,
    )

    messages.success(request, "Comment added.")
    return redirect("polls:results", pk=question.id)

    

        
        
