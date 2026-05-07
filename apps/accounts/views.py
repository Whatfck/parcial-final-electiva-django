from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods


class ProjectLoginView(LoginView):
    template_name = "registration/login.html"


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    return ProjectLoginView.as_view()(request)


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect("home")


def home(request):
    return render(request, "home.html")
