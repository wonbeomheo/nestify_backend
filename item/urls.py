from django.urls import path
from .views import CreateListItem, CreateListPropertyValue, DeleteRetrieveItem

urlpatterns = [
  path('', CreateListItem.as_view(), name='create_list_items'),
  path('<int:id>', DeleteRetrieveItem.as_view(), name='delete_retrieve_item'),
  path('properties/values', CreateListPropertyValue.as_view(), name='create_list_property_value'),
]