from django import forms
from django.utils import timezone
from .models import Tweet, Comment, Poll, PollOption, Event

class TweetForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': "What's happening?",
            'class': 'form-control'
        }),
        max_length=280,
        required=True
    )
    image = forms.ImageField(required=False)

    class Meta:
        model = Tweet
        fields = ['content', 'image']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': "Tweet your reply",
            'class': 'form-control'
        }),
        max_length=280,
        required=True
    )

    class Meta:
        model = Comment
        fields = ['content']

class PollForm(forms.ModelForm):
    question = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': "Ask a question...",
            'class': 'form-control'
        }),
        max_length=140,
        required=True
    )

    duration = forms.ChoiceField(
        choices=[
            (1, '1 day'),
            (3, '3 days'),
            (7, '1 week'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial=1
    )

    class Meta:
        model = Poll
        fields = ['question']

    def save(self, tweet=None, commit=True):
        poll = super().save(commit=False)
        if tweet:
            poll.tweet = tweet

        # Set end date based on duration
        duration_days = int(self.cleaned_data['duration'])
        poll.end_date = timezone.now() + timezone.timedelta(days=duration_days)

        if commit:
            poll.save()
        return poll

class PollOptionForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': "Option",
            'class': 'form-control'
        }),
        max_length=140,
        required=True
    )

    class Meta:
        model = PollOption
        fields = ['text']

PollOptionFormSet = forms.formset_factory(
    PollOptionForm,
    extra=2,
    min_num=2,
    max_num=4,
    validate_min=True,
    validate_max=True
)

class EventForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': "Event title",
            'class': 'form-control'
        }),
        max_length=100,
        required=True
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': "Event description",
            'class': 'form-control'
        }),
        max_length=500,
        required=True
    )

    location = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': "Location",
            'class': 'form-control'
        }),
        max_length=100,
        required=True
    )

    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        required=True
    )

    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        required=True
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("End date must be after start date")

            if start_date < timezone.now():
                raise forms.ValidationError("Start date cannot be in the past")

        return cleaned_data

    def save(self, tweet=None, commit=True):
        event = super().save(commit=False)
        if tweet:
            event.tweet = tweet

        if commit:
            event.save()
        return event
