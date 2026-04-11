from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect

@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        return redirect('home')

    return render(request, 'dashboard/seller/dashboard.html')