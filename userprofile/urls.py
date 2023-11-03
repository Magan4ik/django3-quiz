from django.urls import path
from userprofile import views

app_name = "userprofile"

urlpatterns = [
    path('', views.profile, name="profile"),
    path('myquizes', views.myquizes, name="myquizes"),
    path('create', views.createquiz, name="createquiz"),
    path("redact", views.redactprofile, name="redactprofile"),
    path('myanswers', views.answers, name="answers"),

]
