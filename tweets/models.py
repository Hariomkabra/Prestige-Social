from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Tweet(models.Model):
    content = models.TextField(max_length=280)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='retweets')
    image = models.ImageField(upload_to='tweet_images', blank=True, null=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.content[:50]

    def get_absolute_url(self):
        return reverse('tweet-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

    def is_retweet(self):
        return self.parent is not None

class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=280)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.tweet}'

class Poll(models.Model):
    tweet = models.OneToOneField(Tweet, on_delete=models.CASCADE, related_name='poll')
    question = models.CharField(max_length=140)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.question

    def is_active(self):
        return timezone.now() <= self.end_date

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=140)

    def __str__(self):
        return self.text

    def votes_count(self):
        return self.votes.count()

class PollVote(models.Model):
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_voted = models.DateTimeField(default=timezone.now)

    class Meta:
        # A user can only vote once per option
        unique_together = ('option', 'user')

    def __str__(self):
        return f'{self.user.username} voted for {self.option.text}'

class Event(models.Model):
    tweet = models.OneToOneField(Tweet, on_delete=models.CASCADE, related_name='event')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title

    def is_upcoming(self):
        return timezone.now() <= self.start_date
