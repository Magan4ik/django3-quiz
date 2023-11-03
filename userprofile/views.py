from django.shortcuts import render, redirect
from account.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from account.models import MyUser, Quiz
from django.contrib.auth.decorators import login_required
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
# Create your views here.


@login_required
def profile(request):
    if request.method == "GET":
        quizs = Quiz.objects.filter(user=request.user)
        len_quizs = len(quizs)
        s = 0
        sc = 0
        for q in quizs:
            sc += q.correct_answers
            for a in q.answers:
                s += len(q.answers[a])
        if s != 0:
            percent = int(round(sc / s, 2) * 100)
        else:
            percent = 100
        url = request.user.get_avatar_url()

        quizs = Quiz.objects.exclude(user=request.user)
        ans = 0
        cor_ans = 0
        for q in quizs:
            for a in q.answers:
                if request.user.username in q.answers[a]:
                    ans += 1
                    if q.check_answer_for_user(request.user.username):
                        cor_ans += 1
        if ans != 0:
            cor_per = int(round(cor_ans / ans, 2) * 100)
        else:
            cor_per = 100

        return render(request, "userprofile\profile.html", {"avatar_url": url,
                                                            "num_of_ans": s,
                                                            "correct_sum": sc,
                                                            "num_of_quizs": len_quizs,
                                                            "per":percent,
                                                            "my_ans": ans,
                                                            "my_cor_ans": cor_ans,
                                                            "my_cor_per": cor_per
                                                            })

@login_required
def createquiz(request):
    if request.method == "GET":
        return render(request, "userprofile/createquiz.html")
    elif request.method == "POST":
        q = request.POST["question"]
        count = int(request.POST["counter"])
        vars = []
        radio = int(request.POST["right_answer"])
        ans = -1
        j = 0
        for i in range(1, count + 1):
            var = request.POST.get(f"variant {i}", None)
            if var:
                vars.append(var)
                if radio == i:
                    ans = j
                j += 1

        # vars = request.POST["variants"].split(" ")
        # ans = int(request.POST["answer"]) - 1
        if 0 <= ans < len(vars):
            quiz = Quiz(user=request.user, question=q, right_answer=ans)
            quiz.tags = request.POST["tags"].split(',')
            quiz.answers = dict()
            for v in vars:
                quiz.answers[v] = list()
            quiz.save()
            #return render(request, "userprofile/createquiz.html", {"err": request.POST["tags"]})
            return redirect("home")
        else:
            return render(request, "userprofile/createquiz.html", {"err": ""})

@login_required
def myquizes(request):
    quizs = Quiz.objects.filter(user=request.user)
    percents_of_correct = list()
    percents_of_answer = list()
    tags = list()
    for q in quizs:
        percents_of_correct.append(q.percent_of_correct())
        per = list()
        for v in q.answers:
            per.append(q.percent_of_answer(v))
        percents_of_answer.append(per)
        tags.append(q.tags)


    return render(request, "userprofile\myquizes.html", {"quizs": quizs,
                                                         "poc": percents_of_correct,
                                                         "poa": percents_of_answer,
                                                         "tag_list": tags})

@login_required
def answers(request):
    quizs = Quiz.objects.all()
    if request.method == "GET":
        test = list()
        corrects = list()
        for q in quizs:
            for i, a in enumerate(q.answers):
                if request.user.username in q.answers[a]:
                    test.append(q)
                    right = q.right_answer
                    if q.check_answer(i):
                        corrects.append([i+1, right+1, "CORRECT"])
                    else:
                        corrects.append([i+1, right+1, "INCORRECT"])
        return render(request, "userprofile/answers.html", {"quizs": test, "cor":corrects})

@login_required
def redactprofile(request):
    user = MyUser.objects.get(username=request.user.username)
    url = user.get_avatar_url()
    if request.method == "GET":
        return render(request, "userprofile/redactprofile.html", {'url':url})
    elif request.method == "POST" and request.POST["form_name"] == "avatar":
        img = request.FILES['file_input']
        if img:
            if "image" in img.content_type:
                img1 = Image.open(img)
                img1 = img1.resize((200, 200), Image.ANTIALIAS)
                image_buffer = BytesIO()
                img1.save(image_buffer, format='PNG')
                new_uploaded_image = InMemoryUploadedFile(
                    image_buffer,
                    None,  # Field name
                    img.name,  # File name
                    'image/png',  # Content type
                    image_buffer.tell,  # Size function
                    None  # Content type extra data (not needed for images)
                )
                user.avatar = new_uploaded_image
                user.save()
                url = user.get_avatar_url()
                mes = new_uploaded_image.name
                return render(request, "userprofile/redactprofile.html", {'url': url, 'mes': mes})
            else:
                mes = "It's not image"
                return render(request, "userprofile/redactprofile.html", {'url': url, 'mes': mes})
    elif request.method == "POST" and request.POST["form_name"] == "username":
        username = request.POST['username']
        if len(username) >= 4:
            try:
                user.username = username
                user.save()
                mes = "your username has been successfully changed"
                return render(request, "userprofile/redactprofile.html", {'url': url, 'mes': mes})
            except IntegrityError:
                mes = "this username is already taken"
                return render(request, "userprofile/redactprofile.html", {'url': url, 'mes': mes})
        else:
            mes = "write at least 4 characters"
            return render(request, "userprofile/redactprofile.html", {'url': url, 'mes': mes})
