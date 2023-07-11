from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, wishlist, Address
from django.db.models import Min, Max
from django.contrib import messages

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    try:
        wish_count = wishlist.objects.filter(user=request.user)
    except:
        messages.warning(request, "You need to be logged in to access your wishlist!!")
        wish_count = 0

    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    return {
        'categories': categories,
        'address': address,
        'vendors': vendors,
        'min_max_price': min_max_price,
        'wish_count': wish_count,
    }