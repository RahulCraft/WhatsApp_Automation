from django.contrib import admin
from .models import MessageTemplate, Contact, MessageLog
# Register your models here.

admin.site.register(MessageTemplate)
admin.site.register(Contact)
admin.site.register(MessageLog)
