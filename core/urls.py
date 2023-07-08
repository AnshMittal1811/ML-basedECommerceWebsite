from django.urls import path
from core.views import (add_ajax_review, category_product_list_view,
                        category_list_view, filter_view, product_detail_view, search_view, tags_list_view, vendor_detail_view,
                        vendor_list_view, 
                        product_list_view, 
                        index)
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
    path("filter-products/", filter_view, name = "filter-product")

]