from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request, 'login_reg_app/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)

    if result[0] == False:
        for tag, error in result[1].iteritems():
            messages.error(request, error, extra_tags=tag) #wut, what is this tag thing for
        return redirect ('/login_reg')

    else:
        request.session['id'] = result[1].id

        return redirect('/wishes')

def login(request):
    result = User.objects.validate_login(request.POST)
    print result

    if result[0] == False:
        for tag, error in result[1].iteritems():
            messages.error(request, error, extra_tags=tag) #wut
        return redirect ('/login_reg')

    else:
        request.session['id'] = result[1].id
        print request.session['id']
        return redirect('/wishes')

#remove this after implementing second app
def success(request):
    if 'username' not in request.session:
        return redirect('/')
    return render(request, 'login_reg_app/success.html')

def logout(request):
    request.session.flush()
    return redirect('/login_reg')
