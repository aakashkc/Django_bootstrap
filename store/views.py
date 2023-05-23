
from django.shortcuts import render,get_object_or_404
from .models import Product , ReviewRating
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ReviewForm
# from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages


# Create your views here.
def store(request, category_slug=None):
    categories=None
    products=None

    if category_slug is not None:
        categories=get_object_or_404(Category, slug=category_slug)
        products=Product.objects.filter(category=categories, is_available=True)
        paginator=Paginator(products, 3)
        page_number=request.GET.get('page')
        paged_products=paginator.get_page(page_number)
        product_count=products.count()
        
    else:


        products=Product.objects.all().order_by("id").filter(is_available='True')
        paginator=Paginator(products, 3)
        page_number=request.GET.get('page')
        paged_products=paginator.get_page(page_number)
        # print(page_number)
        # print(paged_products)
        # print(paginator)

        
        


        product_count=products.count()

    # print('return', products)
    # print()

    context= {
        'products': paged_products,
        'product_count':product_count,

        }

   
   
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product= Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request), product_id=single_product).exists() # to check whether the single product is exists in cart or not
        # return HttpResponse(in_cart)
        # exit()
    except Exception as e:
        raise e

    context={'single_product':single_product,
            'in_cart':in_cart,
            }




    return render(request,  'store/product_detail.html', context )

def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword: # this is here it proceed further if anything inside keyword
            products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count=products.count()
        
        context={
                "products": products,
                "product_count": product_count,
                }

    return render (request, 'store/store.html', context)


def submit_review(request, product_id):
    url=request.META.get('HTTP_REFERER') #this will store the current/previous page url 
    if request.method == 'POST':
        try:
            reviews=ReviewRating.objects.get(user__id=request.user.id,  product__id=product_id)
            form=ReviewForm(request.POST, instance=reviews) #we are passing is because we want to check if there is already a review then it upadte with latest review
            # in case if we dnt pass instance by default it will create new review
            form.save()
            messages.success(request, "thank you for your review")
            return redirect(url)
            
        except ReviewRating.DoesNotExist:
            form=ReviewForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                
                data.product_id=product_id
                data.user_id=request.user.id
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review=form.cleaned_data['review']
                data.ip=request.META.get('REMOTE_ADDR')
                data.save()
                messages.success(request, "thank you for your review")
                return redirect(url)
            
                
                    