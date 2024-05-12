from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#A Subject has its course code and its demand
#A Student has its name and the Subjects they want

class College(models.Model):
    college_name =models.CharField(max_length=200, default="")
    college_abbrev = models.CharField(max_length=200, default="")
    def __str__(self):
        return self.college_abbrev
    
class DegreeProgram(models.Model):
    degree_title = models.CharField(max_length=200, default="")
    degree_abbbrev = models.CharField(max_length=200, default="")
    college = models.ForeignKey(College,on_delete=models.CASCADE, null= True, blank=True)
    def __str__(self):
        return self.degree_title
    
class Department(models.Model):
    department_name = models.CharField(max_length=200, default="")
    department_abbrev = models.CharField(max_length=200, default="")
    college = models.ForeignKey(College,on_delete=models.CASCADE, null= True, blank=True)
    def __str__(self):
        return self.department_abbrev
    
class Semester(models.Model):
    semester = models.CharField(max_length=200)
    def __str__(self):
        return self.semester

class Subject(models.Model):
    subject_name = models.CharField(max_length= 200, default='')
    subject_code = models.CharField(max_length= 200, default='')
    def __str__(self):
        return self.subject_code

class Course(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, null= True, blank=True)
    subject_code = models.ForeignKey(Subject, on_delete=models.CASCADE, null= True, blank=True)
    course_code = models.CharField(max_length= 200)
    course_title = models.CharField(max_length= 200)
    course_description = models.CharField(max_length= 450, default="")
    demand = models.IntegerField(default= 0)
    is_elective = models.BooleanField(default= False)
    units = models.IntegerField(default= 3)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null= True, blank=True)
    sem_offered = models.ManyToManyField(Semester, related_name="semester_subs", blank=True)
    prereqs = models.ManyToManyField('self', symmetrical=False, blank=True)
    can_COI = models.BooleanField(default=False)
    
    first_prio = models.IntegerField(default= 0)
    second_prio = models.IntegerField(default= 0)
    third_prio = models.IntegerField(default= 0)
    fourth_prio = models.IntegerField(default= 0)
    
    class Meta:
        unique_together = ['subject_code', 'course_code']
    def __str__(self):
        return f'{self.subject_code.subject_code} {self.course_code}'
    def delete(self, *args, **kwargs):
        # Delete all references to this course in the many-to-many relationships
        self.sem_offered.clear()  # Clear sem_offered many-to-many relationship
        self.prereqs.clear()  # Clear prereqs many-to-many relationship

        # Call the parent class delete method to delete the course instance
        super().delete(*args, **kwargs)
class Student(AbstractUser):
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=200, default="", unique=True)
    priority_level = models.IntegerField(default=1)
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")
    username = models.CharField(max_length=200, default="")
    student_deg_prog = models.CharField(max_length= 200)
    batch = models.CharField(max_length=4,default='2020')
    shopping_cart = models.ManyToManyField(Course, related_name="students",blank=True)
    deg_prog = models.ForeignKey(DegreeProgram, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username
    
class Petition(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null= True, blank=True)
    poster = models.ForeignKey(Student, on_delete=models.CASCADE, null= True, blank=True)
    date_created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=250, default="")

class Report(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=9)
    pdf_file = models.FileField(upload_to='reports/')
    title = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=250, default='')
    upload_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.academic_year} - {self.semester}"