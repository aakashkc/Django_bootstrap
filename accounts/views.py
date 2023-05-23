from email.message import EmailMessage
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import Account
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
#verification email settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from cart.views import _cart_id
from cart.models import Cart
from cart.models import CartItem
import pip._vendor.requests 
import requests
# Create your views here.

def register(request):
    if request.method=="POST":
        form= RegistrationForm(request.POST)
        if form.is_valid():
            first_name= form.cleaned_data["first_name"] #cleaned data is used to fetch the valid value from the request 
            last_name= form.cleaned_data["last_name"]
            phone_number= form.cleaned_data["phone_number"]
            email= form.cleaned_data["email"]
            password= form.cleaned_data["password"]
            username=email.split("@")[0]
            
            user=Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number=phone_number
            user.save()
            
            #user activation email
            
            current_site=get_current_site(request)
            mail_subject="please activate your account"
            message=render_to_string("accounts/account_verification_email.html",{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),})
            to_email=email
            send_email=EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, "Thankyou for registering. we have send you and email verification activation link . please verify with your email address")
            return redirect ('/accounts/login/?command=verification&email=' + email) # this is to dispaly same register page after successfully registering
            
        
    else:
            form=RegistrationForm( )
    context={
                    'form':form,
        }
    return render(request, 'accounts/register.html', context)


@csrf_exempt
def login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        
        user=auth.authenticate(email=email,password=password)  
        
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists() #this is to check whether there is cartitem exists  or not in cart
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)
                    print("hello variatipns")
                    #getting product variation by cart id
                    product_variation=[ ] #making a list of product_variation so that we can add variation like color: green ,size: small.inside this list
                    for item in cart_item:
                        variation=item.variation.all()
                        
                        product_variation.append(list(variation)) # by default variation is queryset so that we have convert it into list before we send it to the production variation list
                    print(product_variation)
                    #get the cart item from the user to access to the product variations
                    print("hello")
                    cart_item=CartItem.objects.filter(user=user)
                    ex_var_list=[ ]
                    id=[ ]
                    for item in cart_item:
                        existing_variation=item.variation.all() #takes all the variations tha are existetd in cart
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                        
                        
                    # product_variation=[1,2,3,4,5,]
                    # ex_var_list=[4,6,5,9]
                    #getting a common variation between products variation and existing variations
                                            
                    for pr in product_variation:
                        if pr in ex_var_list:  
                            index=ex_var_list.index(pr)
                            item_id=id[index]
                            item=CartItem.objects.get(id=item_id)
                            item.quantity +=1
                            item.user=user
                            item.save()
                        else: 
                            cart_item=CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()
                    

            except:
                pass
            auth.login(request,user)
            messages.success(request, "you are now logged in")        
            url=request.META.get('HTTP_REFERER') # it will  grab the previous url from where we came .. not came fromrequest library
            try:
                query=requests.utils.urlparse(url).query
                print("query is ", query)  
                #next=/cart/checkout/
                parms = dict(x.split("=") for x in query.split("&")) #i.e next will be a key and /cart/checkout/ will be a value
                print(parms)
                if "next" in parms:
                    nextpage=parms["next"] #way to access value inside dictonary through dictonary key
                    return redirect(nextpage)
                
            except:
                return redirect('dashboard') 
                pass
                
        else:
            messages.error(request, 'Invalid username or password')
            return redirect("login")
        
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logout")
    return redirect('login')
    
    # return render(request, 'accounts/logout.html')


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request, "Cogratulation you Token is now active ")
        return redirect("login")
    else:
        messages.error(request,"Envalid Actiation links")
        return redirect("register")
        
        
@login_required(login_url='login')
def dashboard(request):
    
    return render(request, "accounts/dashboard.html")



def forgotPassword(request):
    
    if request.method == 'POST':
        email=request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            
            
            #reset passwoard email
            current_site=get_current_site(request)
            mail_subject="please reset your password"
            message=render_to_string("accounts/reset_password_email.html",{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),})
            to_email=email
            send_email=EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request, ' password reset email sent successfully to your email address')
            return redirect('login')
        else:
            messages.error(request, 'account doesnot exists ')      
            return redirect('forgotPassword')      
    
    return render(request, "accounts/forgotpassword.html")

def resetpassword_validate(request, uidb64, token):
        try:
            uid=urlsafe_base64_decode(uidb64).decode()
            user=Account._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user=None
            
        if user is not None and default_token_generator.check_token(user,token):
            request.session['uid']=uid #save the uid inside a session
            messages.success(request,"Please reset your password")
            return redirect('resetPassword')
        
        else:
            messages.error(request, "This link has ben expired")
            return redirect('login')
            
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password) # set passeword in builtin function that take the password and save it in hash formate
            user.save()
            messages.success(request, 'Password has been reset succesfully')
            return redirect('login')    
        else:
            messages.error(request,' Password dont Match')
            return redirect('resetPassword')    
    else:
            return render(request,'accounts/resetpassword.html')
        
    
    
    
    
         
    