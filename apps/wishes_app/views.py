from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse # need to import reverse when using named routes!
from django.contrib import messages
from ..login_reg_app.models import User
from .models import Wish
from django.db.models import Q

# Create your views here.
def index(request):
        # if statement to check if user is currently in session
        # return redirect ('/')

    user = User.objects.get(id=request.session['id'])
    allwishes = Wish.objects.filter(Q(created_by=user)| Q(joined_by=user))
    otherwishes = Wish.objects.exclude(Q(created_by=user)| Q(joined_by=user))

    context = {
        'cur_user' : user,
        'all_wishes' : allwishes,
        'other_wishes' : otherwishes
    }

    return render(request, 'wishes_app/index.html', context)


def add_page(request):
    #send user to the page to add a new item
    return render(request, 'wishes_app/add.html')

#had to change session stuff (add userId var), cant access session from within model
def add_item(request):
    user_id = request.session['id']
    result = Wish.objects.validate(request.POST, user_id)

    if result[0] == False:
        for tag, error in result[1].iteritems():
            messages.error(request, error, extra_tags=tag) #wut, what is this tag thing for
            print result[1]
        return redirect ('/wishes/add_page')

    else:
        # user = User.objects.validate_registration(request.POST)
        # request.session['username'] = request.POST['username']
        return redirect('/wishes')

def display(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    wish_buddies = Wish.objects.get(id=wish_id).joined_by.all()

    print wish_buddies

    context = {
        'wish' : wish,
        'wish_buddies' : wish_buddies
    }

    return render(request, 'wishes_app/display.html', context)

def join(request, wish_id):
    #queries to add an existing wish item to your wish list
    user = User.objects.get(id=request.session['id'])
    addwish = Wish.objects.get(id=wish_id)

    addwish.joined_by.add(user)
    addwish.save()
    return redirect ('/wishes')

def remove(request, wish_id):
    #queries to remove an existing wish item from your wish list
    user = User.objects.get(id=request.session['id'])
    removewish = Wish.objects.get(id=wish_id)

    removewish.joined_by.remove(user)
    removewish.save()
    return redirect('/wishes')

def delete(request, wish_id):
    #queries to delete a wish item you created
    user = User.objects.get(id=request.session['id'])
    creator = Wish.objects.get(id=wish_id).created_by
    deletewish = Wish.objects.get(id=wish_id)

    if user == creator:
        deletewish.delete()
        return redirect('/wishes')
    else:
        return redirect('/wishes')
