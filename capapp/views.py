from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Student, Guardian, StudentPrev, Teacher


@login_required
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
        return redirect('/login/')
    
    return render(request, 'blog/register.html')
@login_required
def teacher_page(request):
    return render(request, 'blog/home.html')

def guardian_page(request):
    guardians = Guardian.objects.all()
    return render(request, 'guardian_list.html', {'guardians': guardians})
@login_required
def all_students_view(request):
    all_global_students = Student.objects.all()
    
    context = {
        'students_data': all_global_students,
        'page_title': 'All Enrolled Students'
    }
    return render(request, 'student_list.html', context)

@login_required
def my_students_view(request):
    try:
        current_teacher = Teacher.objects.get(teacher=request.user)
        my_assigned_students = StudentPrev.objects.filter(teacher=request.user)
    except Teacher.DoesNotExist:
        my_assigned_students = StudentPrev.objects.none()
    
    context = {
        'students_data': my_assigned_students,
        'page_title': 'My Assigned Roster'
    }
    return render(request, 'blog/student_list.html', context)

@login_required
def student_scan(request):
    return render(request, 'student_scan.html')

@login_required
def student_list(request):
    assigned_students = StudentPrev.objects.all() 
    return render(request, 'student_list.html', {'students_data': assigned_students, 'page_title': 'All Assigned Previews'})
