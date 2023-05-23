from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product,  Variation 
from .models import Cart, CartItem 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request, product_id):
    current_user=request.user
    # getting product
    product=Product.objects.get(id=product_id)#get the product which comes through users request through url
    
    if current_user.is_authenticated:   # checking whether users is authenticated
         #getting product variation
        product_variation=[] #making a list of product_variation so that we can add variation like color: green ,size: small.inside this list
        if request.method == "POST":
            for item in request.POST: #if there is color=red in request.post
                key = item  # color will be store as key
                value = request.POST[key] # red will store as value 
                # print(key, value)
            #now checking if the variations comming from POST request are  recorded in database or not 
                try:
                    variation=Variation.objects.get(product=product, variation_category__iexact=key,  variation_value__iexact=value) # if YES then
                    # print(variation)
                    product_variation.append(variation) #append the comming variation from POST request to  PRODUCT_VARIATION list
                except:
                    pass
        # print(product_variation)
        print(f"index of product_variation is {product_variation} ")

    
 

    #getting  Cart Item here
        is_cart_item_exists=CartItem.objects.filter(product=product, user=current_user).exists() #this is to check whether there is cartitem exists  or not in cart

        if is_cart_item_exists: # this says if there is cartitem in cart let go further
            cart_item=CartItem.objects.filter(product=product, user=current_user) # it will return cart_item objects
            # we need 
            # existing  variation => comming from databse i.e  from cart
            #current variation    =>  comming from product_variation
            #cart_item_id => comming from databse i.e  from cart


            #there can be multiple existing variation so making a list for them
            existing_variation_list=[ ]
            id=[ ] #list of id of Cart_item inside cart
            for item in cart_item:
                existing_variation=item.variation.all() # it takes all the variation of  cart_items which is already existed in cart
                existing_variation_list.append(list(existing_variation)) #making existing_variation as list because it is queryset.so before we append existing_variation we should convert it into list
                id.append(item.id)


            print(existing_variation_list)
            #check if a current variation i.e product_variation  is inside the existing variation then we are goiing to increase the cart item quantity
            if product_variation in existing_variation_list:
                #increase cart_item quantity if it is true i.e
                #comming down the line what turns out is  product_varition already became existing variation so 
                # below the queryset  called as index will take out the index number of current product varation form existing_variation_list.
                index=existing_variation_list.index(product_variation) #return index number of product variation from existing_variation_list and where indexno is always  start from zero
                # so after getting index number what we can do is we can get id number of that current product variation
                item_id=id[index]
                item=CartItem.objects.get(product=product, id=item_id) # getting item or cartitem  by matching product and id from database I.e from CartItem
                item.quantity+=1
                item.save()


            else:
                item=CartItem.objects.create(product=product, quantity=1, user=current_user)

                if  len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation) #i.e adding all production variation

                item.save()
        else :
            cart_item=CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if  len(product_variation) > 0:
                    cart_item.variation.clear()          
                    cart_item.variation.add(*product_variation)
            
            cart_item.save()

        # return HttpResponse(cart_item.quantity)
        # exit()

        return redirect('cart') #now redirect to the url whose name is 'cart' basiaclly redirect to one function to another
        
    else: #if user is not logged or authenticated
        

        #getting product variation
        product_variation=[ ] #making a list of product_variation so that we can add variation like color: green ,size: small.inside this list
        if request.method == "POST":
            for item in request.POST: #if there is color=red in request.post
                key = item  # color will be store as key
                value = request.POST[key] # red will store as value 
                # print(key, value)
            #now checking if the variations comming from POST request are  recorded in database or not 
                try:
                    variation=Variation.objects.get(product=product, variation_category__iexact=key,  variation_value__iexact=value) # if YES then
                    # print(variation)
                    product_variation.append(variation) #append the comming variation from POST request to  PRODUCT_VARIATION list
                except:
                    pass
        # print(product_variation)
        print(f"index of product_variation is {product_variation} ")

    
    #getting Cart here
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

    #getting  Cart Item here
        is_cart_item_exists=CartItem.objects.filter(product=product, cart=cart).exists() #this is to check whether there is cartitem exists  or not in cart

        if is_cart_item_exists: # this says if there is cartitem in cart let go further
            cart_item=CartItem.objects.filter(product=product, cart=cart,) # it will return cart_item objects
            # we need 
            # existing  variation => comming from databse i.e  from cart
            #current variation    =>  comming from product_variation
            #cart_item_id => comming from databse i.e  from cart


            #there can be multiple existing variation so making a list for them
            existing_variation_list=[ ]
            id=[ ] #list of id of Cart_item inside cart
            for item in cart_item:
                existing_variation=item.variation.all() # it takes all the variation of  cart_items which is already existed in cart
                existing_variation_list.append(list(existing_variation)) #making existing_variation as list because it is queryset.so before we append existing_variation we should convert it into list
                id.append(item.id)


            print(existing_variation_list)
            #check if a current variation i.e product_variation  is inside the existing variation then we are goiing to increase the cart item quantity
            if product_variation in existing_variation_list:
                #increase cart_item quantity if it is true i.e
                #comming down the line what turns out is  product_varition already became existing variation so 
                # below the queryset  called as index will take out the index number of current product varation form existing_variation_list.
                index=existing_variation_list.index(product_variation) #return index number of product variation from existing_variation_list and where indexno is always  start from zero
                # so after getting index number what we can do is we can get id number of that current product variation
                item_id=id[index]
                item=CartItem.objects.get(product=product, id=item_id) # getting item or cartitem  by matching product and id from database I.e from CartItem
                item.quantity+=1
                item.save()


            else:
                item=CartItem.objects.create(product=product, quantity=1, cart=cart)

                if  len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation) #i.e adding all production variation

                item.save()
        else :
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if  len(product_variation) > 0:
                    cart_item.variation.clear()          
                    cart_item.variation.add(*product_variation)
            
            cart_item.save()

        # return HttpResponse(cart_item.quantity)
        # exit()

        return redirect('cart') #now redirect to the url whose name is 'cart' basiaclly redirect to one function to another


def remove_cart(request,product_id, cart_item_id):
    product=get_object_or_404(Product, id=product_id)
    try:
            if request.user.is_authenticated:
                cart_item=CartItem.objects.get(user=request.user, product=product, id=cart_item_id)
                
            else:
                    cart=Cart.objects.get(cart_id=_cart_id(request)) #to get cart  
                    cart_item=CartItem.objects.get(cart=cart, product=product, id=cart_item_id)

            if cart_item.quantity >1:
                cart_item.quantity -=1
                cart_item.save()
            else:
                cart_item.delete()
    except:
        pass
    return redirect('cart')



def remove_cart_items(request, product_id,cart_item_id):
    product=get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        
        cart_item=CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        # print("return",cart_item, cart)
    else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        
            cart_item=CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            # print("return",cart_item, cart)

    cart_item.delete()

    return redirect('cart')
    













def cart(request, total=0, quantity=0, cart_items=0):


    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        


    }
    
    return render(request, 'store/cart.html',context )



@login_required(login_url='login')
def checkout(request,  total=0, quantity=0, cart_items=0):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
                cart_items=CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        
    }
    return render(request, 'store/checkout.html',context)
