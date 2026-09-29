from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import SignUpForm


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # this triggers the post_save signal -> creates UserProfile
            user.profile.role = form.cleaned_data["role"]
            user.profile.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")    