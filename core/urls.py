from django.urls import path

from .views import index, challenges, scoreboard, register, login_view,logout_view

urlpatterns = [
    path("", index, name="index"),
    path("challenges/", challenges, name="challenges"),
    path("scoreboard/", scoreboard, name="scoreboard"),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]