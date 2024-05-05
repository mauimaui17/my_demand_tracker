from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Course, Student, DegreeProgram
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
import datetime
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from collections import defaultdict
from django.db.models import Count
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper
# Create your views here.
def index(request):
    all_courses = Course.objects.all()
    return render(request, 'tracker/index.html', {'course_list': all_courses})

def homepage(request):
    all_courses = Course.objects.all().order_by('-demand')[:5]
    return render(request, 'tracker/homepage.html', {'course_list': all_courses})
def coursepage(request):
    try: 
        course_id = request.GET.get('course_id')
        course = Course.objects.get(id= course_id)
        deg_prog_pop = Student.objects.filter(shopping_cart__id=course_id)
        breakdown = {}

        deg_prog_counts = deg_prog_pop.values('student_deg_prog').annotate(count=Count('id'))

        # Iterate over the queryset and populate the breakdown dictionary
        for deg_prog_count in deg_prog_counts:
            deg_prog = deg_prog_count['student_deg_prog']
            count = deg_prog_count['count']
            breakdown[deg_prog] = count

        return render(request, 'tracker/course.html', {'course': course, 'users': deg_prog_pop, 'breakdown': breakdown})
    except Exception as e:
        error_message = f"Error: {str(e)}"  # Ensure error_message is properly formatted
        return HttpResponse("<script>alert('An error occured.'); window.location.href='/';</script>")
        #return JsonResponse({"message": error_message})
    except Course.DoesNotExist:
        return HttpResponse("<script>alert('Course not found');  window.location.href='/';</script>")
def profile(request):
    return render(request, 'tracker/profile.html')

@ajax_login_required
def addToCart(request):
    course_id = request.GET.get('course_id')
    try:
        cart = request.user.shopping_cart.all()
        course = Course.objects.get(id=course_id)
        if course not in cart:
            course.demand+=1
            if request.user.priority_level == 1:
                course.first_prio+=1
            elif request.user.priority_level == 2:
                course.second_prio+=1
            elif request.user.priority_level == 3:
                course.third_prio+=1
            elif request.user.priority_level == 4:
                course.fourth_prio+=1
            course.save()
            request.user.shopping_cart.add(course)
            return JsonResponse({"message": "Demand has been updated. Subject added to cart.", "demand": course.demand, "priorities": [course.first_prio, course.second_prio, course.third_prio, course.fourth_prio]})
        else:
            return JsonResponse({"message": "Already in cart.", "demand": course.demand,  "priorities": [course.first_prio, course.second_prio, course.third_prio, course.fourth_prio]})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status="400")
    
@ajax_login_required
def removeFromCart(request):
    course_id = request.GET.get('course_id')
    try:
        cart = request.user.shopping_cart.all()
        course = Course.objects.get(id=course_id)
        if course in cart:
            course.demand-=1
            if request.user.priority_level == 1:
                course.first_prio-=1
            elif request.user.priority_level == 2:
                course.second_prio-=1
            elif request.user.priority_level == 3:
                course.third_prio-=1
            elif request.user.priority_level == 4:
                course.fourth_prio-=1
            course.save()
            request.user.shopping_cart.remove(course)
            return JsonResponse({"message": "Demand has been updated. Subject removed from cart.", "demand": course.demand,  "priorities": [course.first_prio, course.second_prio, course.third_prio, course.fourth_prio]})
        else:
            return JsonResponse({"message": "Course not in cart.", "demand": course.demand})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status="400")
    
def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        #saves a student object, then copies the student name to the username field
        #for django's username-focused authorization which requires username field to exist and be unique.
        if form.is_valid():
            try:
                form.save()
                student = Student.objects.get(email=form.cleaned_data['email'])
                student.username = student.first_name + " " + student.last_name
                # student.student_id = form.cleaned_data['student_id']
                student.batch = student.student_id[:4]
                prio = datetime.date.today().year - int(student.batch)
                if(prio >= 4):
                    student.priority_level = 1
                elif prio == 3:
                    student.priority_level = 2
                elif prio == 2:
                    student.priority_level = 3
                elif prio <= 1:
                    student.priority_level = 4
                student.deg_prog = DegreeProgram.objects.get(degree_title=student.student_deg_prog)
                student.save()
                
                return redirect("/")
            except IntegrityError:
                # Handle duplicate student ID error
                
                messages.error(request, "A student with this ID already exists.")
    else:
        form = RegisterForm()
    return render(request, "registration/signup.html", {"form":form})

