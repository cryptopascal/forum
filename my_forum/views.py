'''
Created on 14 nov. 2012

@author: naamane.othmane
'''

from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.template import RequestContext
from my_forum.forms import *
from django.contrib.auth.decorators import login_required

def main_page(request):
    return render_to_response('index.html',RequestContext(request))


def register_page(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                                            username = form.cleaned_data['username'],
                                            password = form.cleaned_data['password'],
                                            email = form.cleaned_data['email']
                                            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
                               
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request,{
                                        'form':form
                                        })
    return render_to_response(
                              'registration/register.html',variables
                              )
@login_required
def save_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread,nada = Thread.objects.get_or_create(title=form.cleaned_data['thread_title'],created_by=request.user)
            post,nada = Post.objects.get_or_create(title=form.cleaned_data['post_title'],
                                                   description = form.cleaned_data['post_description'],
                                                   created_by=request.user
                                                   )
    else:
        form = ThreadForm()
    variables = RequestContext(request,{
                                        'form':form
                                        })
    return render_to_response('thread_save.html',variables)
    
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')