from django.conf import settings
from django.contrib import admin
from djforms.scholars.models import *
from django.http import HttpResponse
from django.utils.encoding import smart_unicode, smart_str

import csv

def get_json(yuri):
    jason = cache.get('%s_api_json' % yuri)
    if jason is None:
        # read the json data from URL
        earl = "%s/%s/?api_key=%s" % (settings.API_PEOPLE_URL,yuri,settings.API_KEY)
        response =  urllib.urlopen(earl)
        data = response.read()
        # json doesn't like trailing commas, so...
        data = data.replace(',]',']')
        jason = json.loads(data)
        cache.set('%s_api_json' % yuri, jason)
    return jason

def get_people(yuri):
    people = cache.get('%s_api_objects' % yuri)
    if people is None:
        jason = get_json(yuri)
        people = {}
        for j in jason:
            p = Person(**j[j.keys()[0]])
            p.id = j.keys()[0]
            people[j.keys()[0]] = p

        cache.set('%s_api_objects' % yuri, people)
    return people

def export_scholars(modeladmin, request, queryset):

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=celebration_of_scholars.csv'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Leader', 'Leader Email', 'Sponsor', 'Other Sponsor', 'Presenters', 'Funding Source', 'Work Type', 'Permission to Reproduce', 'Faculty Sponsor Approval', 'Table', 'Electricity', 'Link','Poster','Date created'])
    for p in queryset:
        link = "http://%s%s" % (settings.SERVER_URL,p.get_absolute_url())
        poster = "http://%s/assets/%s" % (settings.SERVER_URL,p.poster_file)
        leader = "%s, %s" % (p.leader.last_name, p.leader.first_name)
        presenters = ""
        for f in p.presenters.all():
            if not f.leader:
                presenters += "%s, %s|" % (f.last_name, f.first_name)
            title = smart_str(p.title, encoding='utf-8', strings_only=False, errors='strict')
            funding = smart_str(p.funding, encoding='utf-8', strings_only=False, errors='strict')
            work_type = smart_str(p.work_type, encoding='utf-8', strings_only=False, errors='strict')
        writer.writerow([title, leader, p.user.email, p.leader.sponsor, p.leader.sponsor_other, presenters[:-1], funding, work_type, p.permission, p.shared, p.need_table, p.need_electricity, link,poster,p.date_created])
    return response
export_scholars.short_description = "Export the selected Celebration of Scholars Submissions"

class PresentationAdmin(admin.ModelAdmin):
    model               = Presentation
    actions             = [export_scholars]
    raw_id_fields       = ("user","updated_by",)
    list_max_show_all   = 500
    list_per_page       = 500
    list_display        = ('title','last_name','first_name','email','sponsor','sponsor_other','get_presenters','funding','work_type','permission','shared','need_table','need_electricity','status','poster','date_created')
    ordering            = ['title','work_type','permission','shared','need_table','need_electricity','status','date_created']
    search_fields       = ('title','user__last_name','user__email','funding')

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        obj.save()

admin.site.register(Presenter)
admin.site.register(Presentation, PresentationAdmin)
