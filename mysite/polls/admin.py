from mysite.polls.models import Poll
from django.contrib import admin
from mysite.polls.models import Choice


class PollAdmin(admin.ModelAdmin):
    #...
    list_display = ('question', 'pub_date', 'was_published_today')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
