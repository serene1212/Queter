from django.urls import path

from .views import PostListView, new_post, update_post, like_toggle, ProfileView, follow_toggle

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('explore/', PostListView.as_view(), name='explore'),
    path('new_post/', new_post, name='new_post'),
    path('update_post/', update_post, name='update_post'),
    path('user/<str:username>/', ProfileView.as_view(), name='profile_view'),
    path('follow_toggle/', follow_toggle, name='follow_toggle'),
    path('like_toggle/', like_toggle, name='like_toggle'),
]
