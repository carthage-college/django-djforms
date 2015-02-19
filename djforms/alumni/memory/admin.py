from django.contrib import admin
from djforms.alumni.memory.models import Questionnaire


class PhotoInline(admin.TabularInline):
    model = Questionnaire.photos.through
    extra = 5

class QuestionnaireAdmin(admin.ModelAdmin):
    model = Questionnaire
    list_display  = (
        'first_name', 'last_name', 'email', 'phone',
        'city', 'state','postal_code'
    )
    search_fields = (
        'last_name', 'email', 'city', 'state','postal_code'
    )

    inlines = [PhotoInline,]
    exclude = ('photos',)

admin.site.register(Questionnaire, QuestionnaireAdmin)
