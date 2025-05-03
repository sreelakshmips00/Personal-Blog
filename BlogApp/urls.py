from django.urls import path
from django.contrib.auth import views as auth_views


from .views import (
    register_view,
    CustomLoginView,
    home_view,
    add_post_view,
    profile_view,
    follow_view,
    unfollow_view,
    delete_post_view,
    update_post_view,
    search_view,
    comment_view,
    follow_from_home_view,
    add_comment
)

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('add/', add_post_view, name='add_post'),
    path('profile/', profile_view, name='profile'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('follow/<str:username>/', follow_view, name='follow'),
    path('unfollow/<str:username>/', unfollow_view, name='unfollow'),
    path('home/follow/<str:username>/', follow_from_home_view, name='follow_from_home'),
    path('post/delete/<int:post_id>/', delete_post_view, name='delete_post'),
    path('post/update/<int:post_id>/', update_post_view, name='update_post'),
    path('comment/<int:post_id>/', add_comment, name='comment'),
    path('search/', search_view, name='search'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
