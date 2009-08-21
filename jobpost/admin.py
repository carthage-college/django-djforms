from django.contrib import admin
from djforms.jobpost.models import *

admin.site.register(Department)
admin.site.register(Post)
admin.site.register(JobApplyForm)

prepopulated_fields = {"slug": ("title",)}
list_display  = ('title', 'publish')
list_filter   = ('publish', 'departments')
search_fields = ('title', 'description')
