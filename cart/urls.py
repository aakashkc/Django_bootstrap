from django.urls import path
from . import views


urlpatterns = [
    path('',  views.cart, name="cart"),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),#we write add_cart in url because we have redirected 'add_cart' function of views to urlname called cart
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart, name='remove_cart'), 
    path('remove_cart_items/<int:product_id>/<int:cart_item_id>/', views.remove_cart_items, name='remove_cart_items'),
    
    path('checkout/', views.checkout, name="checkout")
    
    
    
    
    
    
    
    





]


