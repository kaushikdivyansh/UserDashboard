from django.shortcuts import render,HttpResponse, redirect
from django.core import serializers
from django.http import JsonResponse
from django.contrib import messages
from .models import *
import json
import bcrypt
import datetime


dt_format = '%m/%d/%Y'
# Create your views here.

def index(request):

    return render(request,'dashboard/index.html')

def signIn(request):
    return render(request,'dashboard/signin.html')

def register(request):
    return render(request,'dashboard/register.html')

def regVal(request):
    # name_errors = User.objects.basic_validator(request.POST)
    # pwd_errors = User.objects.pwd_validator(request.POST)
    # if (len(name_errors)):
    #     for key,value in name_errors.items():
    #         messages.error(request,value,extra_tags=key)
    # if (len(pwd_errors)):
    #     for key,value in pwd_errors.items():
    #         messages.error(request,value,extra_tags=key)
    #     return redirect('/regVal')

    if User.objects.filter(email = request.POST['email']).count() > 0:
        messages.error(request,"This email is already registered!",extra_tags='email')
        return redirect('/regVal')

    # User.objects.create(first_name=request.POST['firstName'],
    #                     last_name = request.POST['lastName'],
    #                     email = request.POST['email'],
    #                     userlevel = 2,
    #                     pwdhash = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt()))
    User.objects.create(email = request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()), firstName = "", lastName = "", gender = "", birthday = datetime.datetime.now(), address = "", city = "", state = "", schoolState = "", major = "", schoolName = "", admin=0)
    request.session['email'] = request.POST['email']
    return redirect('/dashboard')

def logVal(request):
    print(request.POST)

    user = User.objects.filter(email = request.POST['email'])
    if user.count() > 0 :
        if bcrypt.checkpw(request.POST['loginpwd'].encode(),user[0].password.encode()):
            request.session['firstName'] = user[0].firstName
            request.session['logUserId'] = user[0].id
            request.session['email'] = request.POST['email']
            if user[0].admin == True:
                return redirect('/admindashboard')
            else:
                return redirect('/dashboard')
    messages.error(request,"Bad Credentials!",extra_tags='login')   
    return redirect('/logVal')

def dashboard(request):
    email = request.session['email']
    allColleges = College.objects.all()
    user=User.objects.get(email = email)
    checklist = Checklist.objects.filter(user = user)
    return render(request,'dashboard/dashboard.html',{'user':user, 'checklist': checklist, "colleges": allColleges})

def new(request):
    return render(request,'dashboard/new.html')

def destroy(request,number):
    b = User.objects.get(id=int(number))
    b.delete()
    return redirect ('/dashboard')

def show(request,number):
    return render(request,'dashboard/show.html')

def edit(request,number):
    context={
        'user': User.objects.get(id=number)
    }
    return render(request,'dashboard/edit.html',context)

def userInfoVal(request):
    print(request.POST)
    # name_errors = User.objects.basic_validator(request.POST)
    # if (len(name_errors)):
    #     for key,value in name_errors.items():
    #         messages.error(request,value,extra_tags=key)
    #     return redirect("/edit/"+number)
    b = User.objects.get(email=request.session['email'])
    b.firstName = request.POST['firstName']
    b.lastName = request.POST['lastName']
    # b.email = request.POST['email']atetime.datetime.strptime(d1, dt_format)
    b.birthday = request.POST['birthday']
    b.address = request.POST['address']
    b.city = request.POST['city']
    b.state = request.POST['state']
    b.schoolState = request.POST['schoolState']
    b.major =   request.POST['major'] 
    b.schoolName = request.POST['schoolName']
    b.gender = request.POST["gender"]
    b.save()
    return redirect('/dashboard')


def userpwdVal(request,number):
    pwd_errors = User.objects.pwd_validator(request.POST)
    if (len(pwd_errors)):
        for key,value in pwd_errors.items():
            messages.error(request,value,extra_tags=key)
            return redirect('/edit')
    b = User.objects.get(id=number)
    b.pwdhash = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt())
    b.save()
    return redirect('/success')


def useredit(request):
    return render(request,'dashboard/useredit.html')


def logout(request):
    request.session.flush()
    return redirect('/')

def success(request):
    return HttpResponse("Routed success successfully!")

def admin(request):
    return render(request, 'dashboard/admin.html')

def admindashboard(request):
    allColleges = College.objects.all()
    allTasks = Task.objects.all()
    return render(request, 'dashboard/admindashboard.html', {"colleges": allColleges, "tasks": allTasks})

def adminCollegeTab(request):
    College.objects.create(name = request.POST['name'], city = request.POST['city'],state = request.POST['state'])
    return redirect('/admindashboard')

def adminTaskTab(request):
    college = College.objects.get(id=request.POST['college'])
    Task.objects.create(college = college, title = request.POST['title'], deadline=request.POST['deadline'])
    return redirect('/admindashboard')

def addChecklist(request):
    user = User.objects.get(email=request.session['email'])
    newcollege = College.objects.get(id=request.POST['college'])
    checklistsToDelete = Checklist.objects.filter(college = newcollege, user = user)
    for checklist in checklistsToDelete:
        checklist.delete()

    collegeTasks = Task.objects.filter(college = newcollege)
    for college in collegeTasks:
        Checklist.objects.create(user = user, college = newcollege, is_completed = False, title = college.title, deadline = college.deadline)
    
    return redirect('/dashboard')

def updateChecklist(request):
    user = User.objects.get(email=request.session['email'])
    tempChecklist = Checklist.objects.filter(user = user)
    for i in tempChecklist:
        newChecklist = Checklist.objects.get(id=i.id)
        newChecklist.is_completed = False
        newChecklist.save()
    for x in request.POST:
        if x != 'csrfmiddlewaretoken':
            checklist = Checklist.objects.get(id=x)
            checklist.is_completed = True
            checklist.save()
    return redirect('/dashboard')
