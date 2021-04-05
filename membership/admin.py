from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Customer
from django.contrib import messages
# Register your models here.


admin.site.site_header = 'NAMASTE Sales and Inventory : ADMIN PANEL'
admin.site.site_title = 'My Site Title'
admin.site.index_title = "Manage your data:"



class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'date_created',)
    list_filter = ('date_created',)


admin.site.register(Customer, CustomerAdmin)
admin.site.unregister(Group)
