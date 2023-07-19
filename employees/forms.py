from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control mt-2'}),
            'position': forms.Select(attrs={'class': 'form-control mt-2'}),
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control mt-2'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mt-2'}),
            'supervisor': forms.TextInput(attrs={'class': 'form-control mt-2', 'list': 'employees'})
        }