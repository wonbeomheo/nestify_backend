from django.contrib import admin
from .models import Item, ItemProperty, ItemPropertyAssignment, ItemPropertyValue, ItemPurchase, RoomItem, Transaction


class ItemPropertyValueInline(admin.TabularInline):
  model = ItemPropertyValue
  extra = 1
  can_delete = True
  

class ItemPropertyAssignmentInline(admin.TabularInline):
  model = ItemPropertyAssignment
  extra = 1
  can_delete = True
  autocomplete_fields = ["property", "value"]
  
@admin.register(ItemProperty)
class ItemPropertyAdmin(admin.ModelAdmin):
  list_display = ("name",)
  search_fields = ("name",)
  inilnes = [ItemPropertyValueInline]
  
@admin.register(ItemPropertyValue)
class ItemPropertyValueAdmin(admin.ModelAdmin):
  list_display = ("property", "value")
  search_fields = ("value",)
  list_filter = ("property",)
  
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
  list_display = ("name", "price", "created_at")
  search_fields = ("name",)
  inlines = [ItemPropertyAssignmentInline]
  
admin.site.register(ItemPurchase)
admin.site.register(RoomItem)
admin.site.register(Transaction)