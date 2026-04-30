from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product

from .models import Category

@login_required
def add_product(request):
    if not request.user.is_seller:
        return redirect('home')

    form = ProductForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.seller = request.user
        product.save()

        # handle selected categories
        form.save_m2m()

        # handle new category
        new_category_name = form.cleaned_data.get("new_category")

        if new_category_name:
            category, created = Category.objects.get_or_create(
                name=new_category_name,
                defaults={'created_by': request.user}
            )
            product.categories.add(category)

        return redirect('seller_dashboard')

    return render(request, 'products/add_product.html', {'form': form})

@login_required
def seller_products(request):
    if not request.user.is_seller:
        return redirect('home')

    products = Product.objects.filter(seller=request.user)

    return render(request, 'products/seller_products.html', {
        'products': products
    })

from .models import Category

@login_required
def edit_product(request, pk):
    product = Product.objects.get(pk=pk, seller=request.user)

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if request.method == "POST" and form.is_valid():
        product = form.save()

        # handle new category
        new_category_name = request.POST.get("new_category")

        if new_category_name:
            category, created = Category.objects.get_or_create(
                name=new_category_name,
                defaults={'created_by': request.user}
            )
            product.categories.add(category)

        return redirect('seller_products')

    return render(request, 'products/edit_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = Product.objects.get(pk=pk, seller=request.user)
    product.delete()
    return redirect('seller_products')

from .models import Product

def product_list(request):
    products = Product.objects.all().order_by('-created_at')

    return render(request, 'products/product_list.html', {
        'products': products,
    })


from .cart import Cart
from django.shortcuts import get_object_or_404

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_detail')

from .models import Product

def cart_detail(request):
    cart = Cart(request)

    cart_items = []
    total = 0

    for product_id, quantity in cart.cart.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'products/cart_detail.html', {
        'cart_items': cart_items,
        'total': total
    })