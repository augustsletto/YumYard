from django.urls import path
from .views import Dashboard, OrderDetails, AddMenu, EditMenu
from . import views

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('orders/<int:pk>/', OrderDetails.as_view(), name='order-details'),
    path('add-menu/', AddMenu.as_view(), name='add-menu'),
    path('edit-menu/', EditMenu.as_view(), name='edit-menu'),
    path('edit-item/<item_id>', views.edit_item, name='edit-item'),
    path('delete-item/<int:pk>/', views.delete_item, name='delete-item'),
]