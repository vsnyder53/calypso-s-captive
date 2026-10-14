from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Student, Guardian, StudentPrev, Teacher
from django.utils import timezone
from .forms import PaymentForm, GuardianForm, StudentForm, Student


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

@login_required
def guardian_page(request):
    guardians = Guardian.objects.all()
    context = {
        'guardians': guardians,
        'page_title': 'All current Guardians'
    }
    return render(request, 'blog/guardian.html', context)


@login_required
def my_students_view(request):
    try:
        current_teacher_profile = Teacher.objects.get(teacher=request.user)
        my_assigned_students = Student.objects.filter(teacher=current_teacher_profile)
        
    except Teacher.DoesNotExist:
        my_assigned_students = Student.objects.none()
    
    context = {
        'students_data': my_assigned_students,
        'page_title': 'My Assigned Roster'
    }
    return render(request, 'blog/student_list.html', context)

def all_students_view(request):
    all_global_students = Student.objects.all()
    
    context = {
        'students_data': all_global_students,
        'page_title': 'All Enrolled Students'
    }
    
    return render(request, 'blog/student_list.html', context)


@login_required
def student_scan(request):
    if request.method == 'POST':
        selected_student_id = request.POST.get('studentID')
        uploaded_file = request.FILES.get('scannedDocument')
                
        messages.success(request, f"Scan processed successfully for student ID: {selected_student_id}!")
        return redirect('student_scan')

    all_students = Student.objects.all().order_by('lastname', 'firstName')
    
    context = {
        'students_list': all_students,
    }
    return render(request, 'blog/student_scan.html', context)

@login_required
def student_list(request):
    assigned_students = StudentPrev.objects.all() 
    return render(request, 'blog/student_list.html', {'students_data': assigned_students, 'page_title': 'All Assigned Previews'})

@login_required
def add_student_view(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student_instance = form.save(commit=False)
            
            try:
                active_teacher_profile = Teacher.objects.get(teacher=request.user)
                student_instance.teacher = active_teacher_profile
            except Teacher.DoesNotExist:
                pass
                
            student_instance.calculate_payment()
            student_instance.save()
            
            messages.success(request, f"Profile successfully enrolled!")
            return redirect('/home/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in field '{field}': {error}")
    else:
        form = StudentForm()
        
    return render(request, 'blog/add_student.html', {'form': form})



def add_guardian_view(request):
    if request.method == "POST":
        form = GuardianForm(request.POST)
        if form.is_valid():
            guardian_instance = form.save()
            
            messages.success(request, f"Guardian profile for {guardian_instance.firstName} successfully created!")
            return redirect('/home/') 
    else:
        form = GuardianForm()
        
    return render(request, 'blog/add_guardian.html', {'form': form})



def add_payment_view(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Extract clean verified database query parameters
            student_profile = form.cleaned_data['student']
            input_date = form.cleaned_data['payment_date']
            student_profile.paymentlast = input_date
            student_profile.calculate_payment()
            student_profile.save()
            messages.success(request, f"Payment recorded successfully for {student_profile.firstName}. Next billing cycle updated!")
            return redirect('/home/')
    else:
        form = PaymentForm()
        
    return render(request, 'blog/add_payment.html', {'form': form})

@login_required
def student_profile_view(request, student_id):
    student_record = get_object_or_404(Student, studentID=student_id)

    context = {
        'student': student_record,
    }
    return render(request, 'blog/student_profile.html', context)