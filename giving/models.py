from django.db import models

class Campaign(models.Model):
    title           = models.CharField(max_length=255)
    description     = models.TextField("Description", help_text="This information will appear above the form.")
    about           = models.TextField("About", help_text="This information will appear in the sidebar next to the form.", null=True, blank=True)
    thank_you       = models.TextField("Thank you", help_text="This information will be appear after the donor successfully submits the form.")
    email_info      = models.TextField("Email instructions", help_text="This information will be sent to the donor.")
    slug            = models.SlugField(max_length=255, verbose_name="Slug", unique=True)

    def __unicode__(self):
        return self.title
