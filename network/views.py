import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView

from .forms import UserRegisterForm
from .models import Post, User


class SignUpView(CreateView):
    form_class = UserRegisterForm
    template_name = 'network/register.html'
    success_url = reverse_lazy('login')


class PostListView(LoginRequiredMixin, ListView):
    queryset = Post.objects.all().order_by("-create_date")
    template_name = "network/index.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        pass

    def get_context_data(self, *, object_list=None, **kwargs):
        pass


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "network/profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        current_user: User = self.request.user
        obj: User = self.get_object()
        if current_user != obj:
            data['has_follow'] = current_user.has_follower(obj)

        return data


@login_required
def new_post(request):
    pass


@login_required
def update_post(request):
    pass


@login_required
def follow_toggle(request):
    pass


@login_required
def like_toggle(request):
    pass
