from .models import Question
from django.db.models import F
import time

class PollViewCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        from django.urls import resolve
        try:
            match = resolve(request.path_info)
            if match.url_name == 'detail' and match.namespace == 'polls':
                question_id = str(match.kwargs.get('pk'))
                if question_id:
                    viewed_polls = request.session.get('viewed_polls', {})
                    print(viewed_polls)
                    current_time = time.time()
                    last_view_time = viewed_polls.get(question_id, 0)
                    print(last_view_time)

                    if current_time - last_view_time > 3600:
                        Question.objects.filter(id=question_id).update(views=F('views') + 1)
                        
                        viewed_polls[question_id] = current_time
                        request.session['viewed_polls'] = viewed_polls
                        request.session.modified = True
        except Exception:   
            pass

        return response