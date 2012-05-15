from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from djforms.core.models import GenericChoice

class Event(models.Model):
    user            = models.ForeignKey(User, related_name="catering_event_user")
    # dates
    created_on      = models.DateTimeField(auto_now_add=True)
    updated_on      = models.DateTimeField("Date updated", auto_now=True)
    extension       = models.CharField("Phone extension", max_length=4)
    # event and sponsor info
    event_name      = models.CharField(max_length=128)
    event_date      = models.DateField(help_text="Allow for a minumum of 3 business days before the day of the event, and a maximum of 180 days.")
    event_start     = models.TimeField("Starts at", help_text="(Format HH:MM am/pm)")
    event_end       = models.TimeField("Ends at", help_text="(Format HH:MM am/pm)")
    building        = models.ForeignKey(GenericChoice, verbose_name="Building name", help_text="Name of the building on campus", related_name="catering_event_building")
    room_number     = models.CharField("Room number or location", max_length=50, help_text="Note: You must confirm through AdAstra that the room is available. If it is a location, use: Lounge, common area, lobby, hallway, foyer, outside, etc. ")
    department      = models.CharField("Sponsoring department", max_length=128)
    coordinator     = models.CharField("Event coordinator", max_length=128, help_text="On site contact before, during, after event")
    purpose         = models.CharField("Purpose of Event", max_length=128, help_text="e.g. student recruitment, development, etc.")
    account_number  = models.CharField("Department account number(s)", max_length=255)
    open_to         = models.ManyToManyField(GenericChoice, verbose_name="Event open to", related_name="catering_event_open_to", null=True, blank=True)
    # facility requirements
    facility_att    = models.CharField("Expected facility attendance", max_length=4)
    housing_att     = models.CharField("Expected housing attendance", max_length=4)
    room_set_up     = models.ManyToManyField(GenericChoice, verbose_name="Room set-up", help_text="Check all that apply.", related_name="catering_event_room_set_up", null=True, blank=True)
    room_set_other  = models.FileField(verbose_name="", upload_to='files/catering/', max_length="255", null=True, blank=True, help_text='If you chose "other" above, please attach a diagram to ensure proper set-up.')
    # table arrangement
    rounds          = models.CharField("Round tables (quantity)", max_length=3, null=True, blank=True)
    eight_rect      = models.CharField("Eight foot rectangle tables (quantity)", max_length=3, null=True, blank=True)
    six_rect        = models.CharField("Six foot rectangle tables (quantity)", max_length=3, null=True, blank=True)
    table_cloth     = models.CharField("Table cloths (quantity)", max_length=3, null=True, blank=True)
    breakout        = models.CharField("Breakout tables (quantity)", max_length=3, null=True, blank=True)
    registration    = models.CharField("Registration tables (quantity)", max_length=3, null=True, blank=True)
    skirting        = models.CharField("Table skirting (quantity)", max_length=3, null=True, blank=True)
    head            = models.CharField("Head tables  (quantity)", max_length=3, null=True, blank=True)
    other_table     = models.CharField("Other", max_length=255, null=True, blank=True)
    # Dining requirements
    dining_att      = models.CharField("Expected dining attendance", max_length=4)
    service_start   = models.TimeField("Service time start", help_text="(format HH:MM am/pm)")
    service_end     = models.TimeField("Service time end", help_text="(format HH:MM am/pm)")
    program_start   = models.TimeField("Program time start", help_text="(format HH:MM am/pm)")
    program_end     = models.TimeField("Program time end", help_text="(format HH:MM am/pm)")
    meal_service    = models.ForeignKey(GenericChoice, related_name="catering_event_meal_service")
    menu_desc       = models.TextField("Menu description")
    other_reqs      = models.CharField("Other requirements", max_length=255, help_text="(e.g. decor, colors, etc.)", null=True, blank=True)
    bar_payment     = models.ForeignKey(GenericChoice, verbose_name="Bar payment options", related_name="catering_event_bar_payment")
    beverages       = models.ManyToManyField(GenericChoice, verbose_name="Beverage requirements", related_name="catering_event_beverages", null=True, blank=True)
    #bev_brands      = models.CharField("Specific beverage labels/brands", max_length="255", null=True, blank=True, help_text="Basic red or white table wine will be served unless otherwise specified. Beer will be served on tap unless specified otherwise. Please include specific labels or brands other than the standard offerings listed above.")
    # equipment
    slide           = models.CharField("Slide projector", max_length=2, null=True, blank=True)
    data_proj       = models.CharField("Data projector", max_length=2, null=True, blank=True)
    overhead        = models.CharField("Overhead projector", max_length=2, null=True, blank=True)
    tv_dvd          = models.CharField("TV/DVD", max_length=2, null=True, blank=True)
    cordless_mic    = models.CharField("Cordless mic", max_length=2, null=True, blank=True)
    fixed_mic       = models.CharField("Fixed mic", max_length=2, null=True, blank=True)
    flip_chart      = models.CharField("Flip chart", max_length=2, null=True, blank=True)
    coat_rack       = models.CharField("Coat rack", max_length=2, null=True, blank=True)
    chalkboard      = models.CharField("Chalkboard", max_length=2, null=True, blank=True)
    laptop          = models.CharField("Laptop", max_length=2, null=True, blank=True)
    table_podium    = models.CharField("Podium (table top)", max_length=2, null=True, blank=True)
    free_podium     = models.CharField("Podium (free standing)", max_length=2, null=True, blank=True)
    screen          = models.CharField("Portable screen", max_length=2, null=True, blank=True)
    other_equip     = models.CharField("Other", max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u'%s: %s, %s' % (self.department, self.user.last_name, self.user.first_name)

    def get_absolute_url(self):
        return "http://%s%s" % (settings.SERVER_URL, reverse("catering_event_detail", args=[self.pk]))

