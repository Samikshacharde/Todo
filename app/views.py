from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo(user=request.user,todo_name=task)
        new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request,'todoapp/todo.html',context)

@login_required
def deletetask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect('home-page')

@login_required
def updatetask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')


def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 4:
            messages.error(request,'Password must be atleast 4 characters')
            return redirect('register')

        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username :
            messages.error(request, 'Username already taken')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.success(request,'User Successfully Registered!')
        return redirect('login')

    return render(request,'todoapp/register.html',{})

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username,password=password)
        if validate_user is not None :
            login(request,validate_user)
            return redirect('home-page')
        else :
            messages.error(request,'Please Register.Your Username does not exists')
            return redirect('login')

    return render(request,'todoapp/login.html',{})

def logoutview(request):
    logout(request)
    return redirect('login')
