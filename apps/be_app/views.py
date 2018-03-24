# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect

from .models import User, Qoute, Favorite

from django.contrib import messages

import bcrypt
# Create your views here.
def index(request):
    return render(request, 'be_app/index.html')

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors): 
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        name = request.POST['name']
        alias = request.POST['alias']
        email = request.POST['email']
        password = request.POST['password']
        dob = request.POST['dob']
        request.session['name'] = name
        hashp = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User.objects.create(name = name, alias = alias, email = email, password = hashp, dob = dob)
        new_user.save()
        # request.session['user_id'] = new_user.id
    return redirect('/qoutes') #to the homepage

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email = email)
        hashp = user.password
        check_pw = bcrypt.checkpw(password.encode(), hashp.encode())
        if check_pw == True:
            request.session['name'] = user.name
            return redirect('/qoutes') #to the homepage
        else:
            return redirect('/qoutes')

def qoutes(request):
    user = User.objects.get(name = request.session['name'])
    user_id = user.id
    all_qoutes = Qoute.objects.all()
    user_favorites = Favorite.objects.filter(user_id = user_id)
    context = {
        'user' : user,
        'user_favorites' : user_favorites,
        'all_qoutes' : all_qoutes,
    }
    return render(request, 'be_app/qoutes.html', context)

def process_qoute(request):
    errors = Qoute.objects.qoute_validator(request.POST)
    user = User.objects.get(name = request.session['name'])
    user_id = user.id
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/qoutes')
    else:
        qouted_by = request.POST['qouted_by']
        message = request.POST['message']
        new_qoute = Qoute.objects.create(qouted_by = qouted_by, message = message, user_id = user_id)
        new_qoute.save()
    return redirect('/qoutes')

def process_favorite(request):
    user_id = request.POST['user_id']
    qoute_message = request.POST['qoute_message']
    qoute_author = request.POST['qoute_author']
    new_favorite = Favorite.objects.create(qoute_author = qoute_author, qoute_message = qoute_message, user_id = user_id)
    new_favorite.save()
    return redirect('/qoutes')

def process_remove(request):
    qoute_id = request.POST['qoute_id']
    favorite_qoute = Favorite.objects.get(id = qoute_id)
    favorite_qoute.delete()
    return redirect('/qoutes')

def user(request, user_id):
    user_info = User.objects.get(id = user_id)
    user_favorites = Favorite.objects.filter(user_id = user_id)
    favorite_count = user_favorites.count()
    context = {
        'favorite_count' : favorite_count,
        'user_favorites' : user_favorites,
        'user_info' : user_info,
    }
    return render(request, 'be_app/user.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')
