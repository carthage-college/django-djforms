from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from djforms.core.models import GenericChoice

class Event(models.Model):
    # dates
    created_on      = models.DateTimeField(auto_now_add=True)
    updated_on      = models.DateTimeField("Date updated", auto_now=True)
    # requested by
    first_name      = models.CharField(max_length=128)
    last_name       = models.CharField(max_length=126)
    email           = models.EmailField()
    extension       = models.CharField(max_length=4)
    # event and sponsor info
    event_name      = models.CharField(max_length=128)
    event_date      = models.DateField()
    start_time      = models.TimeField("Starts at", help_text="(format HH:MM am/pm)")
    end_time        = models.TimeField("Ends at", help_text="(format HH:MM am/pm)")
    building        = models.ForeignKey(GenericChoice, verbose_name="Building name", help_text="Name of the building on campus", related_name="dining_event_building")
    room_number     = models.CharField("Room number or location", max_length=50, help_text="If location, use: Lounge, common area, lobby, hallway, foyer, etc. ")
    department      = models.CharField("Sponsoring department", max_length=128)
    coordinator     = models.CharField("Event coordinator", max_length=128, help_text="on site contact before, during, after event")
    purpose         = models.CharField("Purpose of Event", max_length=128, help_text="e.g. student recruitment, development, etc.")
    account_number  = models.CharField("Department account number(s)", max_length=255)
    open_to         = models.ManyToManyField(GenericChoice, verbose_name="Event open to", related_name="dining_event_open_to")
    # facility requirements
    facility_att    = models.CharField("Expected facility attendance", max_length=4)
    housing_att     = models.CharField("Expected housing attendance", max_length=4)

    def __unicode__(self):
        return u'%s: %s %s' % (self.department, self.last_name, self.first_name)

    def get_absolute_url(self):
        return "http://%s%s" % (settings.SERVER_URL, reverse("dining_event_request_detail", args=[self.pk]))

    """
    high_school_science         = models.TextField(max_length=128, help_text="Please list all high school science courses that you have completed.")
    biology_chemistry_courses   = models.TextField("Biology/Chemistry Courses", help_text="Please describe the biology and/or chemistry courses you have taken.")
    research_experience         = models.TextField(help_text="Please describe any research experience.")
    program_interest            = models.TextField(help_text='Please describe why you are interested in the program.')

    """
