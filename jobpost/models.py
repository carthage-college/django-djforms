# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models import permalink

from djforms.core.models import GenericChoice, YEAR_CHOICES

import datetime
from tagging.fields import TagField

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
    address             = models.CharField(max_length=255, verbose_name = 'Address', help_text="Use the campus building name here if the job is on campus.")
    city                = models.CharField(max_length=128, verbose_name = 'City', default="Kenosha")
    state               = models.CharField(max_length=100, verbose_name = 'State', default="Wisconsin")
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
    type_of_job         = models.ForeignKey(GenericChoice, related_name="post_type_of_job")
    transportation      = models.BooleanField('Does this job require transportation to an off-campus site? (Check if yes)')
    description         = models.TextField('Job Description')
    purpose_of_job      = models.TextField('Purpose of the Job')
    duties_resp         = models.TextField('Duties and Responsibilities')
    qualifications      = models.TextField('Qualifications')
    publish             = models.DateTimeField(help_text="A date for the post to go live on")
    expire_date         = models.DateTimeField(help_text="A date for the post to expire on")
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    active              = models.BooleanField(help_text='Is active?', default=False)
    tags                = TagField(help_text="A comma separated list of key words used for the search function.")
    creator             = models.ForeignKey(User, null=True, blank=True)
    
    class Meta:
        permissions = ( ("can_manage", "can manage"), )
        db_table  = 'job_posts'
        ordering  = ('-id',)
        get_latest_by = 'publish'
        
    def __unicode__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ('post_detail', None, {'pid'  : self.id})

    @permalink
    def get_edit_url(self):
        return ('post_manage', None, {'pid'  : self.id})
        
class JobApplyForm(models.Model):
    """ Job Apply Form """
    apply_date   = models.DateTimeField(auto_now_add=True)
    first_name   = models.CharField(max_length=255)
    last_name    = models.CharField(max_length=255)
    email        = models.EmailField()
    address      = models.TextField(verbose_name = 'College Address', help_text="(include Room and Dorm, or Street, City, State)")
    phone        = models.CharField(max_length=12)
    college_id   = models.CharField("Carthage ID", max_length="7")
    college_year = models.CharField("Current Year at Carthage", max_length="1", choices=YEAR_CHOICES)
    major        = models.CharField(max_length=255)
    hours        = models.TextField(verbose_name = 'Hours Available', help_text="What hours are you available to work Sunday through Saturday?")
    app_details  = models.TextField(verbose_name = 'What qualifications do you have for this job?')
    cv           = models.FileField(u'Résumé', upload_to='files/jobs/cvs/', max_length="256", help_text=u'Many employers are requiring a résumé for consideration for their job postings. Pleae include this in your application. If you don not have one, please contact the Writing Center or the Career Center to help you create or update it.', null=True, blank=True)
    job          = models.ForeignKey(Post, null=True, blank=True)

    def render_email(self):
        obj_text =  'First Name:   %s\n' % self.first_name
        obj_text += 'Last Name:    %s\n' % self.last_name
        obj_text += 'Email:     %s\n' % self.email
        obj_text += 'Application submitted on:    %s\n' % self.apply_date
        obj_text += '\nApplication Details:\n\n%s\n\n' % self.app_details
        return obj_text
        
    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)