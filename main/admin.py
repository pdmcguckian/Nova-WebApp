from django.contrib import admin
from .models import PersonalProject, StructuredProjectContent, StructuredProjectCode, StructuredProject
# Register your models here.

class StructuredProjectAdmin(admin.ModelAdmin):
    fieldsets = [
                ("Details", {"fields":["title", "description", "slug"]}),
                ("Content", {"fields":[]}),
                ]


class StructuredProjectContentAdmin(admin.ModelAdmin):
    fields = ['slug', 'step', 'video_link', 'instructions', 'default_code']


class PersonalProjectAdmin(admin.ModelAdmin):
    fields = ["user", "title", "description", "code"]


class StructuredProjectCodeAdmin(admin.ModelAdmin):
    fields = ["user", "project", "code", "step"]


admin.site.register(StructuredProject, StructuredProjectAdmin)
admin.site.register(StructuredProjectContent, StructuredProjectContentAdmin)
admin.site.register(PersonalProject, PersonalProjectAdmin)
admin.site.register(StructuredProjectCode, StructuredProjectCodeAdmin)

