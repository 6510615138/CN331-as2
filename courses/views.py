from django.shortcuts import render
from .models import Course, Register
from users.models import Scholar

# Create your views here.
def index(request):
    return render(request, 'courses/index.html')

def user_page(request):
    if request.user.is_staff == True:
        return render(request, 'courses/user_page.html',
            { 'username':request.user, 'admin':request.user.is_staff,})
    
    scholar_user = Scholar.objects.get(ID=request.user) 
    return render(request, 'courses/user_page.html',
        { 'username':request.user, 'admin':request.user.is_staff,
          'name':scholar_user.get_name(), 'email':scholar_user.get_email(),})

def course_page(request):
    all_course = Course.objects.all()
    reg = Register.objects.filter(reg_scholar_id=request.user)
    reg = reg.values_list('reg_course_id', flat=True)
    return render(request, 'courses/course_page.html',
        { 'username':request.user, 'admin':request.user.is_staff,
          'courses' :all_course,   'scholar':reg,})
    
def board_page(request):
    scholar_course = Register.objects.filter(reg_scholar_id=request.user)
    courses = Course.objects.filter(ID__in=scholar_course.values_list('reg_course_id', flat=True))
    return render(request, 'courses/board_page.html',
        { 'username':request.user, 'admin': request.user.is_staff, 'courses':courses,})

def request_quota(request):
    if request.user.is_staff == True:
        return course_page(request)
    course_select = Course.objects.get(ID=request.POST['reg_course_id'])
    if course_select.course_status == True:
        course_select.course_seat -= 1
    if course_select.course_seat == 0 :
        course_select.course_status = False
    course_select.save()
    scholar_course_select = Register(reg_scholar_id=request.user, reg_course_id=course_select)
    scholar_course_select.save()
    return course_page(request)

def cancel_quota(request):
    course_select = Course.objects.get(ID=request.POST['reg_course_id'])
    course_select.course_seat += 1
    if course_select.course_seat > 0 and course_select.course_status == False:
        course_select.course_status = True
    course_select.save()
    if request.user.is_staff:
        scholar_user = Scholar.objects.get(ID=request.POST['user_id'])
        scholar_course_select = Register.objects.get(reg_scholar_id=scholar_user, reg_course_id=course_select)
        print(scholar_course_select)
        scholar_course_select.delete()
        return management(request)
            
    scholar_course_select = Register.objects.get(reg_scholar_id=request.user, reg_course_id=course_select)
    scholar_course_select.delete()
    return board_page(request)

def management(request):
    print(request.method)
    
    if Course.objects.all().count() == 0:
        return render(request, 'courses/management.html', {
            'username': request.user, 'admin': request.user.is_staff,
            'courses': None, 'register': None, 'all_course': Course.objects.all()})
    
    if request.method == "GET":
        post = Course.objects.all()[:1].get()
        reg = Register.objects.filter(reg_course_id=post.ID)
        reg = Scholar.objects.filter(ID__in=reg.values_list('reg_scholar_id', flat=True))
        return render(request, 'courses/management.html', {
            'username':request.user, 'admin':request.user.is_staff,
            'courses': post, 'register':reg, 'all_course': Course.objects.all(),})  
    post = Course.objects.get(ID=request.POST['reg_course_id'])
    reg = Register.objects.filter(reg_course_id=post.ID)
    reg = Scholar.objects.filter(ID__in=reg.values_list('reg_scholar_id', flat=True))
    return render(request, 'courses/management.html', {
        'username':request.user, 'admin':request.user.is_staff,
        'courses': post, 'register':reg, 'all_course': Course.objects.all(),}) 