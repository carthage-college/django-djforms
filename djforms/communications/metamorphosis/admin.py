from django.contrib import admin

from djforms.communications.metamorphosis.models import Questionnaire


class PhotoInline(admin.TabularInline):
    model = Questionnaire.photos.through
    extra = 5

class QuestionnaireAdmin(admin.ModelAdmin):
    model = Questionnaire
    list_display  = (
        'your_name', 'student_name', 'hometown', 'email'
    )
    search_fields = (
        'your_name', 'student_name', 'hometown', 'email'
    )

    inlines = [PhotoInline,]
    exclude = ('photos',)

admin.site.register(Questionnaire, QuestionnaireAdmin)
