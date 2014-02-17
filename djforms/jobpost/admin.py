from django.contrib import admin
from djforms.jobpost.models import *
from djforms.jobpost.forms import *

class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display  = ('title', 'num_positions','pay_grade','hiring_department','publish','expire_date','creator','active')
    list_filter   = ('publish', 'hiring_department')
    search_fields = ('title', 'description')
    raw_id_fields = ('creator',)

admin.site.register(Post, PostAdmin)
admin.site.register(JobApplyForm)

