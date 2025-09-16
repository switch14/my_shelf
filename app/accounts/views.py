from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse
from django.contrib.auth import login,get_user_model
from .forms import SignUpForm

# Create your views here.

User = get_user_model()

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "accounts/signup.html"

    def get_success_url(self):
        return reverse("book_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
