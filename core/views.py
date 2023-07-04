from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count

from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, wishlist, Address


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
    products = Product.objects.filter(category=product.category).exclude(p_id = p_id)
    p_images = product.p_images.all()

    context = {
        'product': product,
        'p_images': p_images,
        'products': products,
    }
    return render(request, "core/product-detail.html", context)
