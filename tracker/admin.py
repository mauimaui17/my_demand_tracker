from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os
import subprocess

def build_pdf_report(queryset):
        # Define table data headers
    data = [["Department", "Subject Code", "Course Code", "Course Title", "Demand", "First","Second","Third","Fourth"]]

    # Populate table data
    for course in queryset:
        data.append([
            course.department,
            course.subject_code.subject_code,
            course.course_code,
            course.course_title,
            course.demand,
            course.first_prio,
            course.second_prio,
            course.third_prio,
            course.fourth_prio,
        ])
    #return build_pdf_report(data)
    # Create a BytesIO buffer to hold the PDF file
    response = HttpResponse(content_type='application/pdf')
    response_content = f'attachment; filename="{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}_report.pdf"'
    response['Content-Disposition'] = response_content

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        # Define styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    date_style = styles["Normal"]

    # Add title
    title_text = "COURSE REPORT"
    title = Paragraph(title_text, title_style)
    date_time_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    date_time = Paragraph(date_time_text, date_style)
    table = Table(data)

    # Add style to the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    # Build elements to be added to the document
    elements = [title, date_time, table]
    # Add table to the document
    doc.build(elements)

    return response

    
class CourseAdmin(admin.ModelAdmin):
    actions = ['generate_report', 'reset_demand']

    def generate_report(self, request, queryset):
        return build_pdf_report(queryset)
    
    generate_report.short_description = "Generate Selected Courses Report"
    
    def reset_demand(self, request, queryset):
        #generate a report of the current state of the database
        current_state = build_pdf_report(Course.objects.all().order_by("department"))
        #create backup of current database state    
        folder_path = './backups/'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        backup_filename = f'{datetime.now().strftime("%Y_%m_%d-%H_%M_%S")}_reset_backup.sql'
        backup_filepath = os.path.join(folder_path, backup_filename)
        try:
            subprocess.run(['pg_dump', '-U', 'postgres', '-p', '5433', '-f', f'{backup_filepath}', 'demand_tracker'])
        except Exception as e:
            self.message_user(request, f"Failed to create database backup: {e}", level='ERROR')
            return
        #reset all demand
        Course.objects.all().update(demand=0, first_prio = 0, second_prio = 0, third_prio = 0, fourth_prio=0)
        #purge all student shopping carts
        for student in Student.objects.all():
            student.shopping_cart.clear()
        
        self.message_user(request, "All carts cleared and demands have been reset.", level='SUCCESS')

    reset_demand.short_description = "Reset Demand and Purge Shopping Carts"
class SubjectAdmin(admin.ModelAdmin):
    actions = ['generate_report']
    
    def generate_report(self, request, queryset):
        courses = []
        for subject in queryset:
            courses.extend(Course.objects.filter(subject_code=subject))
        
        #print(courses)
        return build_pdf_report(courses)
        #return courses
    
    generate_report.short_description = "Generate Selected Subject Report"

class DepartmentAdmin(admin.ModelAdmin):
    actions = ['generate_report']
    
    def generate_report(self, request, queryset):
        courses = []
        for department in queryset:
            courses.extend(Course.objects.filter(department=department))
        #print(courses)
        return build_pdf_report(courses)
        #return courses
    
    generate_report.short_description = "Generate Selected Department Report"
admin.site.register(Course, CourseAdmin)
admin.site.register(Subject, SubjectAdmin) 
#admin.site.register(Course) 
admin.site.register(Semester)
admin.site.register(College)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(DegreeProgram)

