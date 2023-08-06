from django.contrib import admin
from . models import *
#from import_export.admin import ImportExportModelAdmin 

# Register your models here.
#class menuAdmin(ImportExportModelAdmin, admin.ModelAdmin):    
class menuAdmin(admin.ModelAdmin):    
    list_filter = ('user', 'parent', 'kinds', 'is_master_menu', 'is_statis_menu',)
    list_display = ['parent', 'name', 'link', 'icon', 'order_menu', 'updated_at']
    search_fields = ('name',)
    ordering = ('kinds','parent_id','order_menu',)

admin.site.register(menu, menuAdmin)