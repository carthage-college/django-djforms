from django.contrib import admin
from djforms.jobpost.models import *
from djforms.jobpost.forms import *

class PostFormModelAdmin(admin.ModelAdmin):
    model = Post
    prepopulated_fields = {'slug': ('title',)}
    list_display  = ('title', 'publish')
    list_filter   = ('publish', 'departments')
    search_fields = ('title', 'description')

admin.site.register(Post)
admin.site.register(JobApplyForm)

