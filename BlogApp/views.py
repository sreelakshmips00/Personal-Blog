from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Follow
from .forms import RegisterForm, PostForm, CommentForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'BlogApp/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'BlogApp/login.html'


@login_required
def home_view(request):
    
    tag_name = request.GET.get('tag')
    posts = Post.objects.all().order_by('-created_at')

    if tag_name:
        posts = posts.filter(tags__name__iexact=tag_name)

    comment_form = CommentForm()

    following_ids = Follow.objects.filter(follower=request.user).values_list('following__id', flat=True)
    suggestions = User.objects.exclude(id__in=following_ids).exclude(id=request.user.id)[:5]

    return render(request, 'BlogApp/home.html', {
        'posts': posts,
        'comment_form': comment_form,
        'tag_name': tag_name,
        'suggestions': suggestions
    
    })


@login_required
def add_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'BlogApp/add_post.html', {'form': form})


@login_required
def profile_view(request, username=None):
    user = get_object_or_404(User, username=username) if username else request.user

    posts = Post.objects.filter(author=user).order_by('-created_at')
    tagged_posts = Post.objects.filter(tagged_users=user).exclude(author=user)
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    followers = Follow.objects.filter(following=user)
    followings = Follow.objects.filter(follower=user)

    comment_form = CommentForm()  # <- add this

    return render(request, 'BlogApp/profile.html', {
        'profile_user': user,
        'posts': posts,
        'tagged_posts': tagged_posts,
        'is_following': is_following,
        'followers': followers,
        'followings': followings,
        'comment_form': comment_form  # <- add this to context
    })



@login_required
def follow_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=username)


@login_required
def unfollow_view(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', username=username)


@login_required
def search_view(request):
    query = request.GET.get('q')
    results = User.objects.filter(username__icontains=query) if query else []
    return render(request, 'BlogApp/search.html', {'results': results})


@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('profile', username=request.user.username)


@login_required
def update_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = PostForm(instance=post)
    return render(request, 'BlogApp/update_post.html', {'form': form})


@login_required
def comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect('home')


@login_required
def follow_from_home_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('home')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))
