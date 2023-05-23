from django.http import JsonResponse
from django.shortcuts import redirect ,render
from cart.models import CartItem
from orders.models import Order, Payment, OrderProduct
from .forms import OrderForm
import datetime
import json
from store.models import Product

#email 
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.

def payments(request):
    body= json.loads(request.body)
    order=Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    # print(body)
    #store transation detain in payment model
    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
        

    )
    payment.save()
    
    order.payment=payment
    order.is_ordered=True
    order.save()
    
    # Move the cartitem to order product table
    
    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct=OrderProduct() #we just created OrderProduct class object here
        orderproduct.order_id=order.id
        orderproduct.payment=payment #this is payment is above payment
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product_id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()
        
        #this is for product variation
        cart_item=CartItem.objects.get(id=item.id)
        product_variation=cart_item.variation.all() #geting variation of particular cart item # i wrote variations it didn't work
        orderproduct=OrderProduct.objects.get(id=orderproduct.id) # get the ordered product on the basis of orderproduct id
        orderproduct.variation.set(product_variation)        
        orderproduct.save() 
        

        #Reduce the quantity  of sold product from stock 
        product=Product.objects.get(id=item.product_id)
        product.stocks -= item.quantity
        product.save()
        
    #clearing the cart after purchasing product
    CartItem.objects.filter(user=request.user).delete()
    
    
    # send order receive email notification
    user=request.user
    mail_subject="Thankyou for you order"
    message=render_to_string("orders/order_recieved_email.html",{
                'user' : user,
                'order' : order,})
    to_email=request.user.email
    send_email=EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    
    
    #send order_number and transation id/payments_id back to senddata method via JsonResponse
    data={
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)
    
    
    
    
    
    
    
    





def place_order(request, total=0, quantity=0):
    current_user=request.user

    #if the cart countis less than or equal to 0 then redirect back to shop
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count <=0:
        return redirect ('store')
    
    grand_total=0
    tax=0
    for cart_item in cart_items:
        total=total+(cart_item.product.price* cart_item.quantity)
        quantity=quantity+cart_item.quantity
    tax = (2*total)/100
    grand_total=total+tax
    
        
    
    
    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            #store all the billing information inside the order table
            
            data=Order() #this is because we need instance of odertable before we store any information inside the order table
            data.user=current_user
            data.first_name=form.cleaned_data['first_name'] #this is how we take field value from request. post
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            print("this sis hello")
            
            
            
            # Generating order number using year, time, day
            yr=int(datetime.date.today().strftime('%Y'))
            mt=int(datetime.date.today().strftime('%m'))
            dt=int(datetime.date.today().strftime('%d'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime('%Y%m%d')
            order_number=current_date + str(data.id)
            data.order_number=order_number
            data.save()
            order=Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context={
                'order': order,
                'cart_items': cart_items,
                'tax': tax,
                'grand_total': grand_total
                
            }
            return render(request, 'orders/payments.html', context=context)
    else:
            return redirect('checkout/')

        

def order_complete(request):
    order_number=request.GET.get('order_number')
    transID=request.GET.get('payment_id')
    
    try:
    
        order=Order.objects.get(order_number=order_number, is_ordered=True)
        order_products=OrderProduct.objects.filter(order_id=order.id)
        
        payment=Payment.objects.get(payment_id=transID)
        
        sub_total=0
        for i in order_products:
            sub_total += i.product_price*i.quantity
            
        
        context={
            'order': order,
            'order_products': order_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'sub_total': sub_total
            
        }
        return render(request, 'orders/order_complete.html', context)
        
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
    
        
    
    
    return render(request, 'orders/order_complete.html', )
    
    
        
        
        
            
        