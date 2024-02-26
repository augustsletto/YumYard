from django.urls import path
from .views import Index, Restaurants, Profile, Cart, About, Menu, MenuSearch, Order, OrderConfirmation, OrderPayConfirmation, contact

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('restaurants/', Restaurants.as_view(), name='restaurants'),
    path('profile/', Profile.as_view(), name='profile'),
    path('cart/', Cart.as_view(), name='cart'),
    path('about/', About.as_view(), name="about"),
    path('menu/', Menu.as_view(), name="menu"),
    path('menu/search', MenuSearch.as_view(), name="menu-search"),
    path('order/', Order.as_view(), name="order"),
    path('order-confirmation/<int:pk>', OrderConfirmation.as_view(), name='order-confirmation'),
    path('payment-confirmation/', OrderPayConfirmation.as_view(), name='payment-confirmation'),
    path('contact/', contact, name='contact'),
]
