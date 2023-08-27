from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from datetime import datetime
from .models import Singer, Vote
from django.shortcuts import render , redirect
from django.db.models import F
from django.utils import timezone
@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return JsonResponse({'message': 'Both username and password are required'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists'}, status=400)

        user = User(username=username)
        user.set_password(password)
        user.save()
        return redirect('login')
    else:
        return render(request, 'register.html')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return render(request, 'login.html', {'message': 'Both username and password are required'})

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  
            return redirect("home") 
        
        else:
            return render(request, 'login.html', {'message': 'Invalid username or password'})

    return render(request, 'login.html', {'message': 'Invalid request'})
def home(request):
    return render(request, 'home.html')

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'logout.html', {'message': 'Logout successful'})
    else:
        return render(request, 'logout.html' , {'message': 'Error logging out'})


@login_required
def vote(request):
    if request.method == 'POST':
        singer_id = request.POST.get('singer')
        user = request.user
        current_datetime = timezone.now()

        try:
            singer = Singer.objects.get(id=singer_id)
        except Singer.DoesNotExist:
            return render(request, 'singer_not_found.html')

        if current_datetime > singer.voting_window_end:
            return render(request, 'voting_closed.html')

        try:
            user_vote = Vote.objects.get(user=user, singer=singer)
        except Vote.DoesNotExist:
            user_vote = None

        if user_vote is not None:
            return render(request, 'already_voted.html')

        vote = Vote(user=user, singer=singer)
        vote.save()

        return render(request, 'vote_recorded.html')

    return redirect('home')



@csrf_exempt
def result(request):
    if datetime.now() < Vote.voting_window_end:
        return render(request, 'voting_still_open.html')

    singers = Singer.objects.all().order_by('-votes')
    result = [{'name': singer.name, 'votes': singer.votes} for singer in singers]

    return render(request, 'result.html', {'result': result})
