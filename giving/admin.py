from django.contrib import admin
from djforms.giving.models import Campaign

class CampaignAdmin(admin.ModelAdmin):
    model = Campaign
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Campaign, CampaignAdmin)
