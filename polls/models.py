import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    views=models.IntegerField(default=0)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    ) 

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    @property
    def total_votes(self):
        return self.choice_set.aggregate(models.Sum('votes'))['votes__sum'] or 0

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
    @property
    def get_percent(self):
        total =  self.question.total_votes
        if total > 0:
            return (self.votes / total) * 100 
        else:
            return 0
        
class Comment(models.Model):
    text = models.CharField(max_length=400)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField("created at")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text
