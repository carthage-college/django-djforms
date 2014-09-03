from django.contrib import admin

from djforms.polisci.wipcs.proposal.models import ProposalContact

class ProposalContactAdmin(admin.ModelAdmin):
    model = ProposalContact
    list_display = (
        'last_name', 'first_name', 'email', 'address1', 'address2', 'city',
        'state', 'postal_code', 'phone', 'submitting'
    )
    ordering = ('-created_at',)
    list_filter = (
        'state','city'
    )
    search_fields = (
        'email,', 'last_name', 'city', 'state', 'postal_code'
    )

admin.site.register(ProposalContact, ProposalContactAdmin)

