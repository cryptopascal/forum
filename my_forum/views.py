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
from my_forum.utils import  *

def main_page(request):
    threads = Thread.objects.all()
    threads_to_template = []
    for t in threads:
        a = ThreadsReport(title =t.title, 
                          slug=t.slug,
                          last_post_user= t.post_set.order_by("-created_at")[0].created_by,
                          replies = t.post_set.count()-1)
        threads_to_template.append(a)
    variables = RequestContext(request,{
                                        'threads': threads_to_template})
    return render_to_response('index.html',variables)


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
            new_thread = Thread.objects.create(title=form.cleaned_data['thread_title'],created_by=request.user)
            post= Post.objects.create(title=form.cleaned_data['post_title'],
                                                   description = form.cleaned_data['post_description'],
                                                   created_by=request.user,
                                                   thread=new_thread
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