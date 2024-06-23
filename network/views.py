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
        return Post.objects.filter(owner__in=self.request.user.followers.all()).order_by("-create_date")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['page_title'] = 'Home' if self.request.path == '/index/' else 'Explore'
        return context


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
    if request.method == 'POST':
        data = json.loads(request.body)
        post_content = data.get('post_content')
        if post_content:
            post = Post.objects.create(text=post_content, owner=request.user)
            return JsonResponse({'post_id': post.id}, status=201)
        return JsonResponse({'error': 'post_content is required'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=400)


@login_required
def update_post(request):
    pass


@login_required
def follow_toggle(request):
    if request.method == 'POST':
        current_user = request.user
        user_id = json.loads(request.body).get('user_id')

        if not User.objects.filter(id=user_id).exists():
            return JsonResponse({'error': 'User does not exist'}, status=404)

        user = User.objects.get(id=user_id)
        if current_user == user:
            return JsonResponse({'error': 'You can not follow yourself :)'}, status=400)

        if user.followers.filter(id=current_user.id).exists():
            user.followers.remove(current_user)
            return JsonResponse({'message': 'User unfollowed'}, status=201)
        else:
            user.followers.add(current_user)
            return JsonResponse({'message': 'User followed'}, status=201)
    return JsonResponse({'error': 'Method not allowed'}, status=400)


@login_required
def like_toggle(request):
    if request.method == 'POST':
        post_id = json.loads(request.body).get('post_id')
        current_user = request.user

        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({'error': 'Post does not exist'}, status=404)

        post = Post.objects.get(id=post_id)
        if post.likes.filter(id=current_user.id).exists():
            post.likes.remove(current_user)
            return JsonResponse({'message': 'Post like removed'}, status=201)
        else:
            post.likes.add(current_user)
            return JsonResponse({'message': 'Post liked'}, status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=400)
