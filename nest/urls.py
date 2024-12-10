from django.urls import path
from .views import CreateNestView, DeleteRetrieveRoomView, RetrieveDeleteNestView, CreateListRoomView

urlpatterns = [
    path('', CreateNestView.as_view(), name="create_list_nest"),
    path('<int:id>', RetrieveDeleteNestView.as_view(), name="retrieve_delete_nest"),
    path('<int:nest_id>/rooms', CreateListRoomView.as_view(), name="create_list_room"),
    path('<int:nest_id>/rooms/<int:room_id>', DeleteRetrieveRoomView.as_view(), name="delete_retrieve_room"),
]
