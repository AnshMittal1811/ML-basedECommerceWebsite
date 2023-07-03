from django.urls import path
from core.views import category_list_view, product_list_view, index
# from core.views import index

app_name = "core"

urlpatterns = [
    path("", index, name = "index"),
    path("products/", product_list_view, name = "product-list"),
    path("category/", category_list_view, name = "category-list"),
]