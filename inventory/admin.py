from django.contrib import admin
from .models import Inventory, Offers, Sales, SalesItem
# Register your models here.

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item_name','category')
    list_filter = ('category', 'stocked_date')


class SalesAdmin(admin.ModelAdmin):
    list_filter = ('date_created',)


class SalesItemAdmin(admin.ModelAdmin):
    list_filter = ('sales','item_id',)



admin.site.site_url = "/dashboard"
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Offers)
admin.site.register(Sales, SalesAdmin)
admin.site.register(SalesItem, SalesItemAdmin)

