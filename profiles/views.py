from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request):
    user = request.user

    # Admin profile
    if user.is_super_admin:
        return render(request, 'profiles/admin_profile.html')

    # Seller profile
    elif hasattr(user, 'profile') and user.profile.role == 'seller':
        return render(request, 'profiles/seller_profile.html')

    # Buyer profile
    return render(request, 'profiles/buyer_profile.html')