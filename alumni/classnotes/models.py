from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from djforms.alumni.directory.models import Contact

"""
Model: Note to your classmates
"""

class Note(models.Model):
    contact             = models.ForeignKey(Contact,verbose_name="Alumna",related_name="note_created_by")
    updated_by          = models.ForeignKey(User,verbose_name="Updated by",related_name="note_updated_by",editable=False,null=True,blank=True)
    created_at          = models.DateTimeField("Date Created",auto_now_add=True)
    updated_at          = models.DateTimeField("Date Updated",auto_now=True)
    content             = models.TextField()
    alumnistatus        = models.BooleanField("Almuni office status",default=False,help_text="Approved by Alumni Office")
    alumnicomments      = models.TextField("Alumni office comments",blank=True,null=True)
    pubstatus           = models.BooleanField("Publication status",default=False,help_text="Approved for publication on web and in Carthaginian")
    pubstatusdate       = models.DateTimeField("Web Publication Date",blank=True,null=True)
    carthaginianstatus  = models.BooleanField("Carthiginian status",default=False,help_text="Published in the Carthaginian")
    picture             = models.ImageField("Photo",max_length=255,upload_to="files/alumni/classnotes/photos",help_text="75 dpi and .jpg only",blank=True,null=True)
    caption             = models.CharField("Caption for the photo",max_length=255,blank=True,null=True)

    class Meta:
        db_table = 'alumni_classnote'
        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def __unicode__(self):
        return "%s, %s (%s)" % (self.contact.last_name, self.contact.first_name, self.contact.classyear)

    def get_edit_url(self):
        #return reverse(change_stage, args=["classnotes", "note", self.id] )
        return "http://%s/forms/admin/classnotes/note/%s/" % (settings.SERVER_URL, self.id)
