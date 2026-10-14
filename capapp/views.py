from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def home_page(request):
    return render(request, 'blog/home.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Login')
            return redirect('/login/')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.error(request, "Invalid Login")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/home/')
    
    return render(request, 'blog/login.html')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        user.set_password(password)
        user.save()
        
        messages.info(request, "Account created Successfully! Please return to login.")
        return redirect('/login/') # Changed to redirect to /login/ directly
    
    return render(request, 'blog/register.html')

def teacher_page(request):
    return render(request, 'capapp/home.html')

def guardian_page(request):
    return render(request, 'capapp/guardian.html')

def student_scan(request):
    return render(request, 'capapp/student_scan.html')

def student_list(request):
    return render(request, 'capapp/student_list.html')
