from django.db import models
from django.contrib.auth.models import AbstractUser
from account.fields import ListField
import json
# Create your models here.

def return_list():
    return list()

class MyUser(AbstractUser):
    avatar = models.ImageField(upload_to='')

    def get_avatar_url(self):
        return self.avatar.url


class Quiz(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    right_answer = models.IntegerField(default=0)
    answers = models.JSONField(default=dict())
    correct_answers = models.IntegerField(default=0, blank=True)
    tags = models.JSONField(default=list())

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def check_answer(self, ans):
        return ans == self.right_answer

    def check_answer_for_user(self, username):
        for i, a in enumerate(self.answers):
            if username in self.answers[a]:
                return self.check_answer(i)

    def set_right_answer(self, ans):
        if ans <= len(self.answers) and ans > 0:
            self.right_answer = ans

    def count_answers(self):
        return sum(len(x) for x in self.answers.values())

    def percent_of_correct(self):
        s = self.count_answers()
        if s > 0:
            return int(round(self.correct_answers / s, 2)*100)
        else:
            return 0


    def add_answer(self, var, user):
        if var in self.answers:
            for i in self.answers:
                if user.username in self.answers[i]:
                    break
            else:
                self.answers[var].append(user.username)

    def percent_of_answer(self, ans):
        s = self.count_answers()
        if s > 0:
            return int(round(len(self.answers[ans]) / s, 2)*100)
        else:
            return 0
