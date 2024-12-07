from django.urls import path
from .views import CreateNestView, RetrieveDeleteNestView

urlpatterns = [
    path('', CreateNestView.as_view(), name="create_list_nest"),
    path('<int:id>', RetrieveDeleteNestView.as_view(), name="retrieve_delete_nest"),
]
