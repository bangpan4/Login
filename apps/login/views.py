from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'index.html')

def create(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            newuser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=password)
            newuser.save()
    return redirect('/')

def login(request):
    user_check = User.objects.filter(email=request.POST['email'])
    for user in user_check:
        if user.email == request.POST['email'] and bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/success')
        else:
            messages.add_message(request, messages.ERROR, "Invalid email or password")
            return redirect('/')

def success(request):
    if 'user_id' in request.session:
        context = {
            "user": User.objects.get(id=request.session['user_id']),
            "user_check": User.objects.all(),
        }
        return render(request,"success.html", context)

def clear(request):
    request.session.clear()
    return redirect('/')