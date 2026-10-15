# capapp/forms.py
from django import forms
from .models import Student, Guardian

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'firstName', 'middleInitial', 'lastname', 'teacher', 'documents', 
            'birthDay', 'authpickupName', 'authpickupphone', 'medicalsummary', 
            'allergies', 'deposit', 'paymentlast', 'paymenttype'
        ]
        
        widgets = {
            'firstName': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'middleInitial': forms.TextInput(attrs={'placeholder': 'M.I.', 'maxlength': '2'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'birthDay': forms.DateInput(attrs={'type': 'date'}),
            'authpickupName': forms.TextInput(attrs={'placeholder': 'Authorized Pickup Full Name'}),
            'authpickupphone': forms.TextInput(attrs={'placeholder': 'Pickup Phone Number'}),
            'medicalsummary': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter medical history notes...'}),
            'allergies': forms.Textarea(attrs={'rows': 2, 'placeholder': 'List known food/drug allergies...'}),
            'deposit': forms.CheckboxInput(attrs={'class': 'form-check-input-custom'}),
            'paymentlast': forms.DateInput(attrs={'type': 'date'}),
            'paymenttype': forms.Select(),
        }


class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = ['student', 'firstName', 'middleInitial', 'lastName', 'phone', 'address', 'city']
        
        widgets = {
            'firstName': forms.TextInput(attrs={'placeholder': 'Enter First Name'}),
            'middleInitial': forms.TextInput(attrs={'placeholder': 'Enter Middle Initial', 'maxlength': '2'}),
            'lastName': forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter Street Address'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter City'}),
            'student': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'style': 'width: 100%; background-color: #050505 !important; border: 1px solid #333333 !important; color: #ffffff !important; padding: 10px 14px; border-radius: 8px; font-size: 11pt;'
            })




class PaymentForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('card', 'Credit/Debit Card'),
        ('transfer', 'Electronic Transfer'),
    ]

    student = forms.ModelChoiceField(
        label="Select Student Profile",
        queryset=Student.objects.all(),
        widget=forms.Select()
    )
    amount = forms.DecimalField(
        label="Payment Amount ($)",
        max_digits=7,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 150.00', 'min': '0.01'})
    )
    payment_date = forms.DateField(
        label="Date of Transaction",
        initial=forms.utils.timezone.now, # Defaults automatically to today's timestamp
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    method = forms.ChoiceField(
        label="Payment Method",
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.Select()
    )
    notes = forms.CharField(
        label="Transaction Notes / Reference",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Check #104, Week 4 tuition'})
    )

