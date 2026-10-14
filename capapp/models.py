import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Teacher(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    assgdStud = models.ForeignKey('StudentPrev', on_delete=models.CASCADE)

    def __str__(self):
        return f"Teacher: {self.teacher.first_name}, {self.teacher.last_name} -> Student: {self.assgdStud.studentName.firstName if self.assgdStud.studentName else 'No Name'}"


class StudentPrev(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    studentName = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='prev_names')
    studentID = models.CharField(max_length=50)
    paymentdue = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    enrolledDate = models.DateField()
    genDate = models.DateField(default=timezone.now)
    allergies = models.CharField(max_length=1000)

    def published(self):
        self.genDate = timezone.now()
        self.save()

    def __str__(self):
        return f"Preview for {self.studentName}"


class Student(models.Model):
    firstName = models.CharField(max_length=100)
    middleInitial = models.CharField(max_length=2, blank=True)
    lastname = models.CharField(max_length=100)
    studentID = models.CharField(
        max_length=50, 
        default=uuid.uuid4, 
        unique=True, 
        editable=False
    )
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    documents = models.ForeignKey(
        'StudentScan', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='student_documents' 
    )
    birthDay = models.DateField()
    authpickupName = models.CharField(max_length=200, blank=True)
    authpickupphone = models.CharField(max_length=20, blank=True) 
    medicalsummary = models.CharField(max_length=1000, blank=True)
    allergies = models.CharField(max_length=1000, blank=True)
    deposit = models.BooleanField(default=False) 
    paymentlast = models.DateField(null=True, blank=True)
    paymenttype = models.CharField(max_length=10, choices=[('weekly', 'Weekly'), ('biweekly', 'Biweekly')], default='weekly')
    nextpayment = models.DateField(null=True, blank=True)

    def calculate_payment(self):
        if self.paymentlast:
            if self.paymenttype == 'weekly':
                self.nextpayment = self.paymentlast + timezone.timedelta(days=7)
            elif self.paymenttype == 'biweekly':
                self.nextpayment = self.paymentlast + timezone.timedelta(days=14)
            self.save()

    def __str__(self):
        return f"{self.firstName} {self.lastname}"


class Guardian(models.Model):
    guardian_id = models.CharField(max_length=100, unique=True, editable=False, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='guardians', null=True)
    firstName = models.CharField(max_length=100)
    middleInitial = models.CharField(max_length=2, blank=True)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    zip_code = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        if not self.guardian_id and self.student:
            current_count = Guardian.objects.filter(student=self.student).count()
            self.guardian_id = f"{self.student.studentID}_{current_count + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Guardian: {self.firstName} {self.lastname} ({self.guardian_id})"


class StudentScan(models.Model):
    student = models.ForeignKey('StudentPrev', on_delete=models.CASCADE)
    pdf_file = models.FileField(
        upload_to='pdf_scans/', 
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"Scan uploaded at {self.uploaded_at.date()}"
