from django.contrib import admin
from .models import StructuredProject, PersonalProject, StructuredProjectContent, StructuredProjectCode
# Register your models here.

class StructuredProjectAdmin(admin.ModelAdmin):
    fieldsets = [
                ("Details", {"fields":["title", "published", "description", "slug"]}),
                ("Content", {"fields":[]}),
                ]


class StructuredProjectContentAdmin(admin.ModelAdmin):
    fields = ['slug', 'step', 'video_link', 'instructions', 'default_code']


class PersonalProjectAdmin(admin.ModelAdmin):
    fields = ["user", "title", "description", "code"]


class StructuredProjectCodeAdmin(admin.ModelAdmin):
    fields = ["user", "project", "code"]


admin.site.register(StructuredProject, StructuredProjectAdmin)
admin.site.register(StructuredProjectContent, StructuredProjectContentAdmin)
admin.site.register(PersonalProject, PersonalProjectAdmin)
admin.site.register(StructuredProjectCode, StructuredProjectCodeAdmin)

