from django.shortcuts import render, redirect
from account.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from account.models import MyUser, Quiz
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from PIL import Image
from PIL import UnidentifiedImageError
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.core import serializers


def home(request):
    return render(request, "account\home.html")


def singupuser(request):
    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "account\singup.html", {"form": form, "err":""})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        #if form.is_valid():
        if request.POST['password1'] == request.POST['password2']:
            #IntegrityError
            #UnidentifiedImageError
            try:
                img = request.FILES["file_input"]
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
                user = MyUser.objects.create_user(request.POST['username'], password=request.POST['password1'], avatar=new_uploaded_image)
                user.save()
                login(request, user)
                return redirect("profile/")
            except IntegrityError:
                return render(request, "account\singup.html", {"form": form, "err": "This username already taken"})
            except UnidentifiedImageError:
                return render(request, "account\singup.html", {"form": form, "err": "Avatar must be PNG image"})
        else:
            return render(request, "account\singup.html", {"form": form, "err": "Passwords didn't match"})
        #else:
        #    return render(request, "account\singup.html", {"form": form, "err": "err"})

def check_username(request):
    user_check = MyUser.objects.filter(username = request.POST["input_value"]).exists()
    if user_check:
        return JsonResponse({"check": False})
    else:
        return JsonResponse({"check": True})


def loginuser(request):
    if request.method == "GET":
        return render(request, 'account/loginuser.html', {"form": AuthenticationForm()})
    elif request.method == "POST":
        user = authenticate(request, username= request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'account/loginuser.html', {"form": AuthenticationForm(), 'error': "Username or password didn't match"})
        else:
            login(request, user)
            return redirect("home")

@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


@login_required
def quizes(request):
    quizs = Quiz.objects.all()
    if request.method == "GET":
        test = list()
        tags = list()
        for q in quizs:
            for a in q.answers:
                if request.user.username in q.answers[a]:
                    break
            else:
                test.append(q)
            for i, tag in enumerate(q.tags):
                if tag not in tags:
                    tags.append(tag)
        serquizs = serializers.serialize('json', test)
        return render(request, "account/quizes.html", {"quizs": test, "tags": tags, "serquizs": serquizs})
    elif request.method == "POST":
        pass

def get_answer(request):
    if request.method == "POST":
        quizs = Quiz.objects.all()
        for q in quizs:
            if str(q.id) == request.POST["form_id"]:
                if request.POST.get("answer", None) != None:
                    for i, a in enumerate(q.answers.keys()):
                        if a == request.POST["answer"] and i == q.right_answer:
                            q.add_answer(a, request.user)
                            q.correct_answers += 1
                            q.save()
                            return JsonResponse({'changed': True, 'correct': True})
                    q.answers[request.POST["answer"]].append(request.user.username)
                    q.save()
                    return JsonResponse({'changed': True, 'correct': False})
                else:
                    return JsonResponse({'changed': False, 'correct': False})
