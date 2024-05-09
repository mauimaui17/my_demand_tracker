from .models import Course, Subject, Department
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def generate_course_report(queryset):
    # Define table data headers
    data = [["Department", "Subject Code", "Course Code", "Course Title", "Course Description"]]

    # Populate table data
    for course in queryset:
        data.append([
            course.department,
            course.subject_code.subject_code,
            course.course_code,
            course.course_title,
            course.course_description
        ])

    # Create a PDF document
    doc = SimpleDocTemplate("courses_report.pdf", pagesize=letter)
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

    # Add table to the document
    doc.build([table])
def generate_subject_report(queryset):
    print("lmao")