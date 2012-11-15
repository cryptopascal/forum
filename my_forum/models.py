'''
Created on 13 nov. 2012

@author: naamane.othmane
'''

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin




class Thread(models.Model):
    """
    this class descibes thread
    """
    slug = models.SlugField(max_length=100, verbose_name=_('slug'), unique=True)
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(User)   
    created_at =models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % (self.title)
    
    def save(self,*args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Thread, self).save(*args, **kwargs)        
    

class Post(models.Model):
    """
    this class descibes posts
    """
    slug = models.SlugField(max_length=100, verbose_name=_('slug'))
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=4000)
    thread =  models.ForeignKey(Thread)  
    created_by = models.ForeignKey(User)   
    created_at =models.DateTimeField(auto_now=True,null=True)

    def __unicode__(self):
        return "%s" % (self.title)

    def save(self,*args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
        
admin.site.register(Post)
admin.site.register(Thread)