from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, UserProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment


def signup_view(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('index')
    else:
        user_form = SignUpForm()
        profile_form = UserProfileForm()
    return render(request, 'cofolio_app/signup.html', {'user_form': user_form, 'profile_form': profile_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'cofolio_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def profile_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'cofolio_app/profile.html', {'form': form})

def index_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'cofolio_app/index.html', {'posts': posts})

@login_required
def post_create_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        Post.objects.create(content=content, author=request.user)
        return redirect('index')
    return render(request, 'cofolio_app/post_create.html')

@login_required
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(content=content, author=request.user, post=post)
        return redirect('post_detail', post_id=post.id)
    return render(request, 'cofolio_app/add_comment.html', {'post': post})

def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    return render(request, 'cofolio_app/post_detail.html', {'post': post, 'comments': comments})
