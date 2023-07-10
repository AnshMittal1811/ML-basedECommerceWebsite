from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Avg
from django.template.loader import render_to_string
from django.contrib import messages

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, wishlist, Address
from core.forms import ProductReviewForms

from paypal.standard.forms import PayPalPaymentsForm
from taggit.models import Tag


# Create your views here.
def index(request):
    # return None, "", render
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published",
                                      featured=True).order_by("-id")


    context = {
        "products": products
    }
    return render(request,
                  'core/index.html',
                  context)


def product_list_view(request):
    products = Product.objects.filter(product_status="published")


    context = {
        "products": products
    }
    return render(request,
                  'core/product-list.html',
                  context)


def category_list_view(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }

    return render(request, 'core/category-list.html', context)


def category_product_list_view(request, c_id):
    category = Category.objects.get(c_id = c_id)
    products = Product.objects.filter(product_status = "published",
                                      category = category)
    context = {
        "category": category,
        "products": products,
    }
    return render(request,
                  "core/category-product-list.html",
                  context)


def vendor_list_view(request):

    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors,
    }
    return render(request,
                  "core/vendor-list.html",
                  context)


def vendor_detail_view(request, v_id):
    vendor = Vendor.objects.get(v_id = v_id)
    products = Product.objects.filter(vendor=vendor,
                                  product_status="published"
                                  )
    context = {
        "vendor": vendor,
        "products": products, 
    }
    return render(request,
                  "core/vendor-detail.html",
                  context)


def product_detail_view(request, p_id):
    product = Product.objects.get(p_id = p_id)
    # product = get_object_or_404(Product, p_id = p_id)
    products = Product.objects.filter(category=product.category).exclude(p_id = p_id).order_by("-date")

    # Getting all reviews
    reviews = ProductReview.objects.filter(product=product)

    average_rating = ProductReview.objects.filter(product=product).aggregate(ratings=Avg('ratings'))

    # Products Review form
    review_form = ProductReviewForms()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    # Products images form
    p_images = product.p_images.all()

    context = {
        'product': product,
        'review_form': review_form,
        'average_rating': average_rating,
        'make_review': make_review,
        'p_images': p_images,
        'reviews': reviews,
        'products': products,
    }
    return render(request, "core/product-detail.html", context)


def tags_list_view(request, tag_slug = None):
    products = Product.objects.filter(product_status = "published").order_by("-id")
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        products = products.filter(tags__in = [tag])
    context = {
        "products": products,
        "tag": tag,
    }
    return render(request, "core/tag.html", context)


def add_ajax_review(request, p_id):
    product = Product.objects.get(p_id = p_id)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product=product,
        review=request.POST["review"],
        ratings=request.POST["ratings"],
    )
    
    context = {
        'user': user.username,
        'review': request.POST["review"],
        'ratings': request.POST["ratings"],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(ratings=Avg("ratings"))
    return JsonResponse(
        {
        'bool': True,
        'context': context,
        'average_reviews': average_reviews,
        }
    )


def search_view(request):
    query = request.GET.get("q")
    # Can also use description__icontains = query
    products = Product.objects.filter(title__icontains = query,).order_by("-date")
    context = {
        "products": products,
        "query": query,
    }

    return render(request, "core/search.html", context)


def filter_view(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published",).order_by("-id").distinct()
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in = categories).distinct()
    if len(vendors) > 0:
        products = products.filter(vendor__id__in = vendors).distinct()

    # context = {
    #     "products": products,
    # }

    data = render_to_string("core/async/product-list.html", {"products": products,})

    return JsonResponse({"data": data})


def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'p_id': request.GET['p_id'],
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data

        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data": request.session['cart_data_obj'],
                         'totalcartitems': len(request.session['cart_data_obj'])})


def cart_view(request):
    cart_total_amount = 0.00
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += float(int(item['qty']) * float(item['price']))
        return render(request, "core/cart.html", {'cart_data': request.session['cart_data_obj'],
                                                  'totalcartitems': len(request.session['cart_data_obj']),
                                                  'cart_total_amount': cart_total_amount,})
    else:
        messages.warning(request, "Your Cart is empty!!")
        return redirect("core:index")
        # return render(request, "core/cart.html", {'cart_data': '',
        #                                           'totalcartitems': len(request.session['cart_data_obj']),
        #                                           'cart_total_amount': cart_total_amount,})


def delete_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0.00
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += float(int(item['qty']) * float(item['price']))

    context = render_to_string("core/async/cart-list.html", {'cart_data': request.session['cart_data_obj'],
                                                             'totalcartitems': len(request.session['cart_data_obj']),
                                                             'cart_total_amount': cart_total_amount,})
            

    return JsonResponse({"data": context,
                         'totalcartitems': len(request.session['cart_data_obj'])})


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0.00
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += float(int(item['qty']) * float(item['price']))

    context = render_to_string("core/async/cart-list.html", {'cart_data': request.session['cart_data_obj'],
                                                             'totalcartitems': len(request.session['cart_data_obj']),
                                                             'cart_total_amount': cart_total_amount,})
            

    return JsonResponse({"data": context,
                         'totalcartitems': len(request.session['cart_data_obj'])})


@login_required
def checkout_view(request):
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '200',
        'item_name': "Order-Item-No-3",
        'invoice': "INVOICE_NO-3",
        'currency_code': "USD",
        'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
        'return_url': 'http://{}{}'.format(host, reverse("core:payment-successful")),
        'cancel_url': 'http://{}{}'.format(host, reverse("core:payment-failed")),
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    cart_total_amount = 0.00
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += float(int(item['qty']) * float(item['price']))
            
        return render(request, "core/checkout.html", {'cart_data': request.session['cart_data_obj'],
                                                      'totalcartitems': len(request.session['cart_data_obj']),
                                                      'cart_total_amount': cart_total_amount,
                                                      'paypal_payment_button': paypal_payment_button})


@csrf_exempt
def payment_completed_view(request):
    context = request.POST
    return render(request, 'core/payment-completed.html', {'context': context})


@csrf_exempt
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')
