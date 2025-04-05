from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Tweet, Comment, Poll, PollOption, PollVote, Event
from .forms import TweetForm, CommentForm, PollForm, PollOptionFormSet, EventForm

class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = 'tweets/home.html'
    context_object_name = 'tweets'
    paginate_by = 10

    def get_queryset(self):
        # Show all tweets for simplicity
        return Tweet.objects.all().order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TweetForm()
        return context

class ExploreView(ListView):
    model = Tweet
    template_name = 'tweets/explore.html'
    context_object_name = 'tweets'
    paginate_by = 10
    ordering = ['-date_posted']

class TweetDetailView(DetailView):
    model = Tweet
    template_name = 'tweets/tweet_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context

class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    form_class = TweetForm
    template_name = 'tweets/tweet_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TweetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tweet
    form_class = TweetForm
    template_name = 'tweets/tweet_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        tweet = self.get_object()
        return self.request.user == tweet.author

class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = 'tweets/tweet_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        tweet = self.get_object()
        return self.request.user == tweet.author

@login_required
def tweet_like(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)

    # Always return a redirect for simplicity
    return redirect('tweet-detail', pk=pk)

@login_required
def retweet(request, pk):
    original_tweet = get_object_or_404(Tweet, id=pk)
    if Tweet.objects.filter(author=request.user, parent=original_tweet).exists():
        messages.warning(request, 'You have already retweeted this tweet.')
    else:
        retweet = Tweet(author=request.user, parent=original_tweet, content=original_tweet.content)
        retweet.save()
        messages.success(request, 'Tweet has been retweeted!')

    return redirect('home')

@login_required
def add_comment(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.tweet = tweet
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('tweet-detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'tweets/add_comment.html', {'form': form})

class SearchView(ListView):
    model = Tweet
    template_name = 'tweets/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            tweet_results = Tweet.objects.filter(content__icontains=query)
            return tweet_results
        return Tweet.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        if query:
            context['users'] = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        return context

@login_required
def insights_view(request):
    """View for the premium insights page"""
    return render(request, 'tweets/insights.html')

@login_required
def create_poll(request):
    """View for creating a poll"""
    if request.method == 'POST':
        tweet_form = TweetForm(request.POST)
        poll_form = PollForm(request.POST)
        option_formset = PollOptionFormSet(request.POST, prefix='options')

        if tweet_form.is_valid() and poll_form.is_valid() and option_formset.is_valid():
            # Save the tweet
            tweet = tweet_form.save(commit=False)
            tweet.author = request.user
            tweet.save()

            # Save the poll
            poll = poll_form.save(tweet=tweet)

            # Save the options
            for form in option_formset:
                if form.cleaned_data.get('text'):
                    option = form.save(commit=False)
                    option.poll = poll
                    option.save()

            messages.success(request, 'Your poll has been created!')
            return redirect('home')
    else:
        tweet_form = TweetForm()
        poll_form = PollForm()
        option_formset = PollOptionFormSet(prefix='options')

    context = {
        'tweet_form': tweet_form,
        'poll_form': poll_form,
        'option_formset': option_formset,
    }

    return render(request, 'tweets/create_poll.html', context)

@login_required
def create_event(request):
    """View for creating an event"""
    if request.method == 'POST':
        tweet_form = TweetForm(request.POST)
        event_form = EventForm(request.POST)

        if tweet_form.is_valid() and event_form.is_valid():
            # Save the tweet
            tweet = tweet_form.save(commit=False)
            tweet.author = request.user
            tweet.save()

            # Save the event
            event = event_form.save(tweet=tweet)

            messages.success(request, 'Your event has been created!')
            return redirect('home')
    else:
        tweet_form = TweetForm()
        event_form = EventForm()

    context = {
        'tweet_form': tweet_form,
        'event_form': event_form,
    }

    return render(request, 'tweets/create_event.html', context)

@login_required
def vote_poll(request, pk):
    """View for voting on a poll"""
    poll = get_object_or_404(Poll, pk=pk)

    if not poll.is_active():
        messages.warning(request, 'This poll has ended.')
        return redirect('tweet-detail', pk=poll.tweet.pk)

    if request.method == 'POST':
        option_id = request.POST.get('option')
        if option_id:
            option = get_object_or_404(PollOption, pk=option_id, poll=poll)

            # Check if user has already voted
            if PollVote.objects.filter(option__poll=poll, user=request.user).exists():
                messages.warning(request, 'You have already voted on this poll.')
            else:
                # Create the vote
                PollVote.objects.create(option=option, user=request.user)
                messages.success(request, 'Your vote has been recorded!')

        return redirect('tweet-detail', pk=poll.tweet.pk)

    return redirect('tweet-detail', pk=poll.tweet.pk)
