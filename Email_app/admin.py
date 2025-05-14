from django.contrib import admin
from .models import EmailEntry

# Register your models here.

@admin.register(EmailEntry)
class EmailEntryAdmin(admin.ModelAdmin):
    list_display = ('region', 'district', 'school_name', 'email','phone_number')
    search_fields = ('region','district','school_name','email','phone_number')

from .models import SMSMessage

@admin.register(SMSMessage)
class SMSMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'message', 'date_added')
    list_filter = ('category', 'date_added', 'user')
    search_fields = ('message', 'user__username')
    ordering = ('-date_added',)
