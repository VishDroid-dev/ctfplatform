from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm

from .models import Challenge, CustomUser, Solve

def index(request):
    return render(request, "index.html")

@login_required
def challenges(request):
    if request.method == "POST":
        flag = request.POST.get("flag")
        challenge = Challenge.objects.filter(flag=flag).first()
        
        if challenge is not None:
            user = request.user
            solve_exists = Solve.objects.filter(user=user, challenge=challenge).exists()

            if not solve_exists:
                user.points += challenge.points
                user.save()
                Solve.objects.create(user=user, challenge=challenge)  # Create a Solve object to track solved challenges
                return render(request, "challenge.html", {"flag": "correct"})
            else:
                return render(request, "challenge.html", {"flag": "Already solved"})
        
        return render(request, "challenge.html", {"flag": "incorrect"})

    return render(request, "challenge.html")


def scoreboard(request):
    users = CustomUser.objects.filter(points__gt=0).order_by('-points')
    return render(request, 'scoreboard.html', {'users': users})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('challenges')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('challenges')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index') 