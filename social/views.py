from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Post
from .forms import PostForm, CommentForm
from .serializers import PostSerializer, CommentSerializer
from .forms import PostForm, CommentForm, ProfileUpdateForm
from .forms import RegistrationForm
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .forms import UserLoginForm
from .models import User, Post, Comment, Profile
from .forms import ProfileForm
from django.contrib.auth import authenticate, login




@login_required
def feed(request):
    # Retrieve posts from users the authenticated user follows
    followed_users = request.user.profile.following.all()
    posts = Post.objects.filter(user__profile__user__in=followed_users).order_by('-created_at')


    if request.method == 'POST':
        # Handle post form submission
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()

    context = {'posts': posts, 'form': form}
    return render(request, 'feed.html', context)





def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Registration successful. Welcome, {username}!')
            return redirect('social:login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


from django.contrib.auth import authenticate, login

# def login_view(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             print('User:', user)  # Print the user object for debugging purposes
#             if user is not None:
#                 login(request, user)  # Log in the user
#                 print('User logged in successfully.')  # Print a message to confirm successful login
#                 messages.success(request, f'Welcome back, {username}!')
#                 return redirect('feed')
#             else:
#                 messages.error(request, 'Invalid username or password.')
#     else:
#         form = UserLoginForm()
#     return render(request, 'login.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print('User:', user)
            if user is not None:
                login(request, user)
                print('User logged in successfully.')
                messages.success(request, f'Welcome back, {username}!')
                return redirect('social:feed')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('social:login')

@login_required
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    followed_users = request.user.profile.following.all()
    context = {'user': user, 'followed_users': followed_users}
    return render(request, 'profile.html', {'user': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('social:profile', user_id=request.user.id)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile_edit.html', {'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('social:feed')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('social:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('social:feed')
    return render(request, 'delete_post.html', {'post': post})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully.')
    return redirect('post_detail.html', post_id=post.id)

@login_required
def user_search(request):
    query = request.GET.get('query')
    results = User.objects.filter(username__icontains=query)

    context = {'results': results}
    return render(request, 'user_search.html', context)

@login_required
def notification(request):
    # Get the notifications for the logged-in user
    notifications = request.user.notifications.all()

    context = {'notifications': notifications}
    return render(request, 'notification.html', context)


class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
