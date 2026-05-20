from django.urls import path
from .views import add_product, seller_products, edit_product, delete_product, product_list
from .views import add_to_cart, remove_from_cart, cart_detail
from .views import categories_view
from .views import category_detail
from .views import product_search
from .views import product_detail

urlpatterns = [
    path('add/', add_product, name='add_product'),
    path('my-products/', seller_products, name='seller_products'),
    path('edit/<int:pk>/', edit_product, name='edit_product'),
    path('delete/<int:pk>/', delete_product, name='delete_product'),
    path('all/', product_list, name='product_list'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('categories/', categories_view, name='categories'),
    path('categories/<int:category_id>/', category_detail, name='category_detail'),
    path('search/', product_search, name='product_search'),
    path('<int:product_id>/', product_detail, name='product_detail'),
]