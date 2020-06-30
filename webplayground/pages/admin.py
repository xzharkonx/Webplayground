from django.contrib import admin
from .models import Page

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')

    # Inyectamos nuestro fichero css
    #Para hacer adaptativo al campo de ckeditor
    #https://gist.github.com/hcosta/15ae0835e5824685d46e75f49efc1bcb
    class Media:
        css = {
            'all': ('pages/css/custom_ckeditor.css',)
        }

admin.site.register(Page, PageAdmin)
