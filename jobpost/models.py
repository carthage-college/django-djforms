from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

from django.db.models import permalink
from tagging.fields import TagField
from tagging.models import Tag
import tagging

import datetime

class Category(models.Model):
    """ Category """
    title       = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True)
  
    class Meta:
        verbose_name_plural = 'categories'
        db_table = 'job_categories'
        ordering = ('title',)
  
    class Admin:
        prepopulated_fields = {'slug': ('name',)}
  
    def __unicode__(self):
        return '%s' % self.title
  
    @permalink
    def get_absolute_url(self):
        return ('category_detail', None, { 'slug':self.slug })

class Post(models.Model):
    """ Post model """
    title       = models.CharField(max_length=255, help_text="The title of the job post")
    slug        = models.SlugField(verbose_name="Slug", unique=True)
    post_manager= models.ForeignKey(User)
    description = models.TextField('Job Description')
    publish     = models.DateTimeField(help_text="A date for the post to go live on")
    expire_date = models.DateTimeField(help_text="A date for the post to expire on")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    categories  = models.ManyToManyField(Category, blank=True)
    tags        = TagField()
    
    class Meta:
        db_table  = 'job_posts'
        ordering  = ('-publish',)
        get_latest_by = 'publish'
    
    class Admin:
        prepopulated_fields = {'slug': ('title',)}
        list_display  = ('title', 'publish')
        list_filter   = ('publish', 'categories')
        search_fields = ('title', 'body')
    
    def __unicode__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ('post_detail', None, {'slug'  : self.slug})

class JobApplyForm(models.Model):
    apply_date  = models.DateTimeField(auto_now_add=True)
    first_name  = models.CharField(max_length=255)
    last_name   = models.CharField(max_length=255)
    email       = models.EmailField()
    app_details = models.TextField(verbose_name = 'What qualifications do you have for this job?')
    job         = models.ForeignKey(Post, null=True, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)
