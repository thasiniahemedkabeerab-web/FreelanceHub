from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FreelancerProfile, Job
from .models import JobApplication

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": ("role",),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {
            "fields": ("role",),
        }),
    )


admin.site.register(FreelancerProfile)
admin.site.register(Job)
admin.site.register(JobApplication)