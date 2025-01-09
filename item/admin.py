from django.contrib import admin
from .models import Item, Property, PropertyAssignment, PropertyValue, ItemPurchased, RoomItemPurchasedAssignment, Transaction


class PropertyValueInline(admin.TabularInline):
  model = PropertyValue
  extra = 1
  can_delete = True
  

class PropertyAssignmentInline(admin.TabularInline):
  model = PropertyAssignment
  extra = 1
  can_delete = True
  autocomplete_fields = ["value"]
  
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
  list_display = ("name",)
  search_fields = ("name",)
  inilnes = [PropertyValueInline]
  
@admin.register(PropertyValue)
class PropertyValueAdmin(admin.ModelAdmin):
  list_display = ("property", "value",)
  search_fields = ("value",)
  list_filter = ("value",)
  
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
  list_display = ("name", "price", "created_at")
  search_fields = ("name",)
  inlines = [PropertyAssignmentInline]
  
admin.site.register(ItemPurchased)
admin.site.register(RoomItemPurchasedAssignment)
admin.site.register(Transaction)