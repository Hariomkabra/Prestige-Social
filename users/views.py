from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from tweets.models import Tweet

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    tweets = Tweet.objects.filter(author=user).order_by('-date_posted')

    is_following = False
    if request.user.is_authenticated and user != request.user:
        is_following = request.user.profile.followers.filter(id=user.id).exists()

    context = {
        'user_profile': user,
        'tweets': tweets,
        'is_following': is_following,
        'followers_count': user.profile.followers.count(),
        'following_count': user.following.count(),
    }

    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/edit_profile.html', context)

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        if request.user.profile in user_to_follow.profile.followers.all():
            user_to_follow.profile.followers.remove(request.user)
            messages.info(request, f'You unfollowed {user_to_follow.username}')
        else:
            user_to_follow.profile.followers.add(request.user)
            messages.success(request, f'You are now following {user_to_follow.username}')
    return redirect('profile', username=username)

class FollowerListView(ListView):
    model = User
    template_name = 'users/followers.html'
    context_object_name = 'users'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user.profile.followers.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Followers'
        context['user_profile'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context

class FollowingListView(ListView):
    model = User
    template_name = 'users/following.html'
    context_object_name = 'users'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user.following.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Following'
        context['user_profile'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')
