from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import get_user_model

from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import get_user_model
from accounts.models import Profile  # 👈 add this

User = get_user_model()


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)

        password = form.cleaned_data.get("password")
        role = form.cleaned_data.get("role")

        user.set_password(password)

        if role == "seller":
            user.is_seller = True
            user.is_buyer = False
        else:
            user.is_buyer = True

        user.save()

        # ✅ safer: ensure profile exists
        profile, created = Profile.objects.get_or_create(user=user)

        profile.role = role

        # auto approve buyers
        if role == "buyer":
            profile.is_approved = True

        profile.save()

        return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})

from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_view(request):
    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        # 🔥 Role-based redirect (important)
        if user.is_super_admin:
            return redirect('admin_dashboard')
        elif user.is_seller:
            return redirect('seller_dashboard')
        else:
            return redirect('buyer_home')

    return render(request, 'accounts/login.html', {'form': form})


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CompleteProfileForm

@login_required
def complete_profile(request):
    # Skip if already completed
    if request.user.profile_completed:
        return redirect('seller_dashboard')

    if request.method == 'POST':
        form = CompleteProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.profile_completed = True
            user.save()
            return redirect('seller_dashboard')
    else:
        form = CompleteProfileForm(instance=request.user)

    return render(request, 'accounts/complete_profile.html', {'form': form})