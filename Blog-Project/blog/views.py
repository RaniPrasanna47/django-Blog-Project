from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Profile
from .forms import PostForm, CommentForm, SignUpForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,"Welcome! Account created.")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request,'blog/signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            messages.success(request,"Logged in.")
            return redirect('home')
        messages.error(request,"Invalid credentials.")
    return render(request,'blog/login.html')

def logout_view(request):
    logout(request)
    messages.info(request,"Logged out.")
    return redirect('home')

def home(request):
    q = request.GET.get('q','').strip()
    posts_qs = Post.objects.select_related('author').annotate(num_comments=Count('comments'))
    if q:
        posts_qs = posts_qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(author__username__icontains=q))
    paginator = Paginator(posts_qs, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    trending = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments','-created_at')[:6]

    # QUICK ADD needs this in context
    post_form = PostForm()
    if request.method == 'POST' and request.user.is_authenticated:
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            p = post_form.save(commit=False)
            p.author = request.user
            p.save()
            messages.success(request,'Post published!')
            return redirect('post_detail', pk=p.pk)

    context = {'posts':posts,'trending':trending,'post_form':post_form,'q':q}
    return render(request,'blog/home.html',context)

def about(request):
    stats = {'total_posts':Post.objects.count(),'total_users':Profile.objects.count()}
    return render(request,'blog/about.html',{'stats':stats})

def contact(request):
    return render(request,'blog/contact.html')

@login_required
def profile(request, username):
    # FIX: never 404 for missing Profile—create it on the fly
    user_obj = get_object_or_404(User, username=username)
    user_profile, _ = Profile.objects.get_or_create(user=user_obj)

    is_owner = request.user.username == username
    posts = Post.objects.filter(author=user_profile.user)

    if request.method == 'POST' and is_owner:
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile updated.")
            return redirect('profile', username=username)
    else:
        form = ProfileForm(instance=user_profile)

    return render(
        request,
        'blog/profile.html',
        {'profile_obj':user_profile, 'posts':posts, 'is_owner':is_owner, 'form':form}
    )

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.select_related('author')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request,"Login to comment.")
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post
            c.author = request.user
            c.save()
            messages.success(request,'Comment added.')
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request,'blog/post_detail.html',{'post':post,'comments':comments,'form':form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.author = request.user
            p.save()
            messages.success(request,"Created.")
            return redirect('post_detail', pk=p.pk)
    else:
        form = PostForm()
    return render(request,'blog/post_form.html',{'form':form,'mode':'Create'})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,"Updated.")
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request,'blog/post_form.html',{'form':form,'mode':'Edit'})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.info(request,'Deleted.')
        return redirect('home')
    return render(request,'blog/post_confirm_delete.html',{'post':post})
