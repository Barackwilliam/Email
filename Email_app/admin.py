from django.contrib import admin
from .models import EmailEntry

# Register your models here.

@admin.register(EmailEntry)
class EmailEntryAdmin(admin.ModelAdmin):
    list_display = ('region', 'district', 'school_name', 'email','phone_number')
    search_fields = ('region','district','school_name','email','phone_number')


