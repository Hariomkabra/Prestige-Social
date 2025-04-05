import os
import random
import requests
import tempfile
from io import BytesIO
from PIL import Image
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.files import File
from users.models import Profile
from tweets.models import Tweet, Comment
from faker import Faker
import shutil

class Command(BaseCommand):
    help = 'Creates dummy users with profiles and tweets'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--tweets', type=int, default=5, help='Number of tweets per user')
        parser.add_argument('--comments', type=int, default=3, help='Number of comments per tweet')

    def handle(self, *args, **options):
        fake = Faker()
        num_users = options['users']
        num_tweets = options['tweets']
        num_comments = options['comments']

        # Create default profile images directory if it doesn't exist
        default_images_dir = os.path.join(settings.BASE_DIR, 'media', 'default_profiles')
        os.makedirs(default_images_dir, exist_ok=True)

        # Copy default.jpg to default_profiles if it doesn't exist
        default_img_path = os.path.join(settings.BASE_DIR, 'media', 'default.jpg')
        if os.path.exists(default_img_path):
            shutil.copy(default_img_path, os.path.join(default_images_dir, 'default.jpg'))

        # Create dummy users
        users = []
        self.stdout.write(self.style.SUCCESS(f'Creating {num_users} dummy users...'))

        # Define some premium professions and locations
        premium_professions = [
            'CEO', 'Entrepreneur', 'Investor', 'Venture Capitalist', 'Executive',
            'Founder', 'Business Owner', 'Director', 'Angel Investor', 'Philanthropist'
        ]

        premium_locations = [
            'New York, USA', 'London, UK', 'San Francisco, USA', 'Dubai, UAE',
            'Singapore', 'Tokyo, Japan', 'Paris, France', 'Hong Kong', 'Sydney, Australia',
            'Toronto, Canada'
        ]

        # Create users with profiles
        for i in range(num_users):
            # Create user
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}"
            email = f"{username}@example.com"

            # Skip if username already exists
            if User.objects.filter(username=username).exists():
                continue

            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123',
                first_name=first_name,
                last_name=last_name,
                date_joined=fake.date_time_between(start_date='-2y', end_date='now', tzinfo=timezone.get_current_timezone())
            )

            # Create profile
            profession = random.choice(premium_professions)
            location = random.choice(premium_locations)

            bio = f"{profession} | {fake.catch_phrase()} | {location}"

            profile = Profile.objects.get(user=user)
            profile.bio = bio
            profile.location = location
            profile.website = fake.url()

            # Download a realistic profile picture
            gender = 'male' if random.random() < 0.5 else 'female'
            try:
                # Use randomuser.me API to get realistic profile pictures
                response = requests.get(f'https://randomuser.me/api/?gender={gender}')
                if response.status_code == 200:
                    data = response.json()
                    if data and 'results' in data and len(data['results']) > 0:
                        picture_url = data['results'][0]['picture']['large']

                        # Download the image
                        img_response = requests.get(picture_url)
                        if img_response.status_code == 200:
                            # Save the image to a temporary file
                            img_temp = BytesIO(img_response.content)
                            img_temp.seek(0)

                            # Generate a filename
                            filename = f"profile_{user.username}.jpg"

                            # Save to profile
                            profile.profile_image.save(filename, File(img_temp), save=False)

                            self.stdout.write(f"Downloaded profile picture for {user.username}")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error downloading profile picture: {e}"))

            # Download a cover image (using unsplash for random beautiful images)
            try:
                cover_categories = ['business', 'office', 'city', 'technology', 'luxury']
                category = random.choice(cover_categories)
                cover_url = f"https://source.unsplash.com/1200x400/?{category}"

                # Download the image
                cover_response = requests.get(cover_url)
                if cover_response.status_code == 200:
                    # Save the image to a temporary file
                    cover_temp = BytesIO(cover_response.content)
                    cover_temp.seek(0)

                    # Generate a filename
                    cover_filename = f"cover_{user.username}.jpg"

                    # Save to profile
                    profile.cover_image.save(cover_filename, File(cover_temp), save=False)

                    self.stdout.write(f"Downloaded cover image for {user.username}")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error downloading cover image: {e}"))

            # Save the profile with the new images
            profile.save()

            users.append(user)
            self.stdout.write(f"Created user: {username} ({first_name} {last_name})")

        # Create dummy tweets
        self.stdout.write(self.style.SUCCESS(f'Creating tweets for each user...'))
        all_tweets = []

        for user in users:
            for _ in range(num_tweets):
                tweet_content = fake.paragraph(nb_sentences=random.randint(1, 3))
                if len(tweet_content) > 280:
                    tweet_content = tweet_content[:280]

                tweet = Tweet.objects.create(
                    content=tweet_content,
                    author=user,
                    date_posted=fake.date_time_between(
                        start_date=user.date_joined,
                        end_date='now',
                        tzinfo=timezone.get_current_timezone()
                    )
                )
                all_tweets.append(tweet)
                self.stdout.write(f"Created tweet for {user.username}: {tweet_content[:50]}...")

        # Create dummy comments
        self.stdout.write(self.style.SUCCESS(f'Creating comments for tweets...'))

        for tweet in all_tweets:
            # Get random users excluding the tweet author
            commenters = random.sample([u for u in users if u != tweet.author], min(num_comments, len(users)-1))

            for commenter in commenters:
                comment_content = fake.sentence()
                if len(comment_content) > 280:
                    comment_content = comment_content[:280]

                Comment.objects.create(
                    content=comment_content,
                    tweet=tweet,
                    author=commenter,
                    date_posted=fake.date_time_between(
                        start_date=tweet.date_posted,
                        end_date='now',
                        tzinfo=timezone.get_current_timezone()
                    )
                )
                self.stdout.write(f"Created comment by {commenter.username} on {tweet.author.username}'s tweet")

        # Create follow relationships
        self.stdout.write(self.style.SUCCESS(f'Creating follow relationships...'))

        for user in users:
            # Each user follows 2-5 random users
            num_to_follow = random.randint(2, min(5, len(users)-1))
            users_to_follow = random.sample([u for u in users if u != user], num_to_follow)

            for user_to_follow in users_to_follow:
                # Add the current user to the followers of the user they're following
                user_to_follow.profile.followers.add(user)
                self.stdout.write(f"{user.username} is now following {user_to_follow.username}")

        # Create likes
        self.stdout.write(self.style.SUCCESS(f'Creating likes for tweets...'))

        for tweet in all_tweets:
            # Each tweet gets 1-8 random likes
            num_likes = random.randint(1, min(8, len(users)-1))
            likers = random.sample([u for u in users if u != tweet.author], num_likes)

            for liker in likers:
                tweet.likes.add(liker)
                self.stdout.write(f"{liker.username} liked {tweet.author.username}'s tweet")

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(users)} users with profiles, {len(all_tweets)} tweets, and comments'))
