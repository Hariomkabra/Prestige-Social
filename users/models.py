from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    cover_image = models.ImageField(default='default_cover.jpg', upload_to='cover_pics')
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Skip image processing if we're in a management command
        import sys
        if 'manage.py' in sys.argv and 'create_dummy_users' in sys.argv:
            return

        # Resize profile image if it exists
        try:
            if self.profile_image and self.profile_image.path:
                img = Image.open(self.profile_image.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_image.path)
        except Exception as e:
            print(f"Error processing profile image: {e}")
