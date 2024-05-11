from django import forms
from .models import Student, DegreeProgram, Report, Course
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import datetime
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email Address')
    #regex validator.
    student_id = forms.CharField(max_length=200, validators=[RegexValidator(
        regex=r'^20\d{2}-\d{5}$',
        message='Student ID must be in the format 20XX-XXXX',
        code='invalid_student_id'
    )], label='Student ID (20XX-XXXXX)')
    student_deg_prog = forms.ModelChoiceField(queryset=DegreeProgram.objects.all(), label='Degree Program')
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email", "password1", "password2", "student_id",'student_deg_prog']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'password1': 'Password',
            'password2': 'Confirm Password',
            'student_id': 'Student ID (20XX-XXXXX)',
            'student_deg_prog': 'Degree Program'
        }
    #checks if the student id is valid.
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        year_part = int(student_id[:4])
        current_year = datetime.date.today().year
        if year_part > current_year:
            raise ValidationError('Year part of student ID cannot be in the future')
        return student_id
    


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email Address')

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email Address'
        self.fields['password'].label = 'Password'
        
class UploadReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['semester', 'academic_year', 'title', 'pdf_file']
        
class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['college','department', 'sem_offered', 'subject_code', 'course_code', 'course_title', 'course_description', 'prereqs', 'can_COI', 'is_elective']