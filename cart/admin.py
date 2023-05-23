from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem

@admin.register(Cart)

class CartAdmin(admin.ModelAdmin):
    list_display=['cart_id','date_added']
    # readonly_field=['cart_id','date_added']
 

    list_filter=('date_added',)
    ordering=('-date_added',)

@admin.register(CartItem)

class CartItemAdmin(admin.ModelAdmin):
    list_display=['id','product','cart','quantity','is_active']
  

    list_filter=('product','is_active')

    






# admin.site.register(Cart)
# admin.site.register(CartItem)



