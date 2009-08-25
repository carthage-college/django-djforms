from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from djforms.core.models import GenericChoice
from django.db.models import permalink
from tagging.fields import TagField
from tagging.models import Tag
import tagging

import datetime

class Department(models.Model):
    """ Department """
    name          = models.CharField(max_length=100, verbose_name = 'Department Name')
    slug          = models.SlugField(unique=True)
    number        = models.CharField(max_length=3, verbose_name = 'Department Number')
    contact_name  = models.CharField(max_length=100, verbose_name = 'Department Contact')
    contact_phone = models.CharField(max_length=100, verbose_name = 'Department Phone')
    
    class Meta:
        verbose_name_plural = 'departments'
        db_table = 'job_departments'
        ordering = ('name',)
  
    class Admin:
        prepopulated_fields = {'slug': ('name',)}
  
    def __unicode__(self):
        return '%s' % self.name
  
    @permalink
    def get_absolute_url(self):
        return ('department_detail', None, { 'slug':self.slug })
        
#uses the generic choice field from the core app
class Post(models.Model):
    """ Post model """
    period              = models.ForeignKey(GenericChoice, related_name="post_period")
    title               = models.CharField(max_length=255, help_text="The title of the job post")
    slug                = models.SlugField(verbose_name="Slug", unique=True, help_text="The slug is automatically generated from the title of the job post as you type, and will form a part of the URL for the job posting (e.g. http://www.carthage.edu/forms/job/math-tutors-needed/). If an error appears for this field, you will have to modify the slug field so that it is unique, as an error indicates that the value of the slug already exists in the system. The easiest way to ensure that the slug is unique is to have a descriptive title or simply add -2 to the end of the slug that is generated from the value of the title field.")
    num_positions       = models.IntegerField(max_length=5, verbose_name = 'Number of Positions Available')
    hours               = models.IntegerField(max_length=5, verbose_name = 'Average Number of Hours Per Week')
    pay_grade           = models.ForeignKey(GenericChoice, related_name="post_pay_grade")
    work_days           = models.ManyToManyField(GenericChoice, verbose_name = 'Student May Have to work', related_name="post_work_days")
    hiring_department   = models.ForeignKey(Department)
    supervisor_name     = models.CharField(max_length=100)
    supervisor_phone    = models.CharField(max_length=100)
    supervisor_email    = models.EmailField()
    displace_employee   = models.BooleanField(verbose_name = 'Does this position displace a full-time employee? (Check if yes)')
    student_supervision = models.BooleanField(verbose_name = 'Do the students you employ have direct supervision by a full-time Carthage employee? (Check if yes)')
    hour_integrity      = models.BooleanField(verbose_name = 'Do you have a system for ensuring that students work the hours that they indicate on their time slip? (Check if yes)')
    description         = models.TextField('Job Description')
    publish             = models.DateTimeField(help_text="A date for the post to go live on")
    expire_date         = models.DateTimeField(help_text="A date for the post to expire on")
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    active              = models.BooleanField(help_text='', verbose_name='Is active?', default=True)
    tags                = TagField(help_text="Used for search.")
    
    class Meta:
        db_table  = 'job_posts'
        ordering  = ('-publish',)
        get_latest_by = 'publish'
        
    def __unicode__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ('post_detail', None, {'slug'  : self.slug})

    @permalink
    def get_edit_url(self):
        return ('post_manage', None, {'slug'  : self.slug})
        
class JobApplyForm(models.Model):
    """ Job Apply Form """
    apply_date  = models.DateTimeField(auto_now_add=True)
    first_name  = models.CharField(max_length=255)
    last_name   = models.CharField(max_length=255)
    email       = models.EmailField()
    app_details = models.TextField(verbose_name = 'What qualifications do you have for this job?')
    job         = models.ForeignKey(Post, null=True, blank=True)
    
    def render_email(self):
        obj_text =  'First Name:   %s\n' % self.first_name
        obj_text += 'Last Name:    %s\n' % self.last_name
        obj_text += 'Email:     %s\n' % self.email
        obj_text += 'Application submitted on:    %s\n' % self.apply_date
        obj_text += '\nApplication Details:\n\n%s\n\n' % self.app_details
        return obj_text
        
    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)
    
