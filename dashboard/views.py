from django.shortcuts import render

# Create your views here.
from datetime import datetime

def get_greeting(user):
    hour = datetime.now().hour

    if hour < 12:
        time = "Good morning"
    elif hour < 18:
        time = "Good afternoon"
    else:
        time = "Good evening"

    return f"{time}, {user.email}"

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from products.models import Product

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.contrib.auth import get_user_model

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Sum

from products.models import Product
from orders.models import Order

User = get_user_model()


@login_required
def admin_dashboard(request):
    if not request.user.is_super_admin:
        return redirect('home')

    total_revenue = Order.objects.aggregate(total_sum=Sum('total'))['total_sum'] or 0

    context = {
        'total_users': User.objects.count(),
        'total_sellers': User.objects.filter(profile__role='seller').count(),
        'total_products': Product.objects.count(),

        'total_orders': Order.objects.count(),
        'total_revenue': total_revenue,

        'recent_users': User.objects.order_by('-date_joined')[:6],
        'recent_orders': Order.objects.order_by('-created_at')[:5],
        'recent_products': Product.objects.order_by('-created_at')[:6],

        'pending_sellers': User.objects.filter(
            profile__role='seller',
            profile__is_approved=False
        ).count(),
    }

    return render(request, 'dashboard/admin/dashboard.html', context)

@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        return redirect('home')

    # Redirect to profile completion if not done yet
    if not request.user.profile_completed:
        return redirect('complete_profile')

    products = Product.objects.filter(seller=request.user)
    my_products = products.order_by('-created_at')[:5]
    total_products = products.count()

    return render(request, 'dashboard/seller/dashboard.html', {
        'my_products': my_products,
        'total_products': total_products,
        'greeting': get_greeting(request.user),
    })

from django.shortcuts import render
from products.models import Product

def buyer_home(request):
    products = Product.objects.all().order_by('-created_at')[:12]

    return render(request, 'dashboard/buyer/buyer_home.html', {
        'products': products
    })