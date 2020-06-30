from django.contrib import admin
from .models import Message

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = ('user','content','created')
    search_fields = ('user__username','content')
    date_hierarchy = 'created'
    list_filter = ('user__username',)

admin.site.register(Message, MessageAdmin)