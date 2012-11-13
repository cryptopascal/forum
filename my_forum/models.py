'''
Created on 13 nov. 2012

@author: naamane.othmane
'''

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify



class Thread(models.Model):
    """
    this class descibes thread
    """
    slug = models.SlugField(max_length=100, verbose_name=_('slug'), unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=4000)
    created_by = models.ForeignKey(User)   
    created_at =models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s" % (self.name)
    
    class Meta:        
        verbose_name = _('Thread')
        verbose_name_plural = _('Threads')
        app_label = 'threads'    
            
    def save(self,*args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Thread, self).save(*args, **kwargs)


class Post(models.Model):
    """
    this class descibes posts
    """
    slug = models.SlugField(max_length=100, verbose_name=_('slug'), unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=4000)
    thread =  models.ForeignKey(Thread)  
    created_by = models.ForeignKey(User)   
    created_at =models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User)   
    updated_at =models.DateTimeField()
    def __unicode__(self):
        return "%s" % (self.title, self.thread)
    
    class Meta:        
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        app_label = 'Post'    
            
    def save(self,*args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)