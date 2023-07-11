from django.urls import include, path
from core.views import (about_us, add_ajax_review, add_to_cart, add_to_wishlist, ajax_contact_form, cart_view, 
                        category_product_list_view, category_list_view, 
                        checkout_view, contact, customer_dashboard, delete_from_cart, 
                        filter_view, make_address_default, order_detail, 
                        payment_completed_view, payment_failed_view, privacy_policy, 
                        product_detail_view, purchase_guide, remove_from_wishlist, 
                        search_view, tags_list_view, terms_of_service, 
                        update_cart, vendor_detail_view,
                        vendor_list_view, 
                        product_list_view, 
                        index, wishlist_view)
# from core.views import index

app_name = "core"

urlpatterns = [

    # Homepage
    path("", index, name = "index"),

    # Products
    path("products/", product_list_view, name = "product-list"),
    path("product/<p_id>/", product_detail_view, name = "product-detail"),

    # Category
    path("category/", category_list_view, name = "category-list"),
    path("category/<c_id>/", category_product_list_view, name = "category-product-list"),

    # Vendor
    path("vendor/", vendor_list_view, name="vendor-list"),
    path("vendor/<v_id>", vendor_detail_view, name="vendor-detail"),

    # Tags
    path("products/tag/<slug:tag_slug>/", tags_list_view, name="tags"),

    # Reviews
    path("add-ajax-review/<p_id>/", add_ajax_review, name="add-ajax-review"),

    # Search Queries
    path("search/", search_view, name = "search"),

    # Async Filtering Products
    path("filter-products/", filter_view, name = "filter-product"),

    # Cart View for Data
    path("add-to-cart/", add_to_cart, name = "add-to-cart"),
    path("cart/", cart_view, name = "cart"),
    path("delete-from-cart/", delete_from_cart, name = "delete-from-cart"),
    path("update-cart/", update_cart, name = "update-cart"),

    # Checkout 
    path("checkout/", checkout_view, name = "checkout"),

    # Payment Integration
    path("paypal/", include("paypal.standard.ipn.urls")),
    path("payment-successful/", payment_completed_view, name = "payment-successful"),
    path("payment-failed/", payment_failed_view, name = "payment-failed"),

    # Customer Dashboard
    path("dashboard/", customer_dashboard, name = "dashboard"),
    path("dashboard/order/<int:id>", order_detail, name = "order-detail"),

    # Making Default Address
    path('make-default-address/', make_address_default, name='make-default-address'),

    # Wishlist Page
    path('wishlist/', wishlist_view, name = "wishlist"),
    path('add-to-wishlist/', add_to_wishlist, name = "add-to-wishlist"),
    path('remove-from-wishlist/', remove_from_wishlist, name = "remove-from-wishlist"),

    path("contact/", contact, name="contact"),
    path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),

    path("about_us/", about_us, name="about_us"),
    path("purchase_guide/", purchase_guide, name="purchase_guide"),
    path("privacy_policy/", privacy_policy, name="privacy_policy"),
    path("terms_of_service/", terms_of_service, name="terms_of_service"),
]