import os
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.conf import settings
import shutil

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Ensure default images exist before creating profile
        ensure_default_images()
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# Create default profile images if they don't exist
def ensure_default_images():
    default_profiles_dir = os.path.join(settings.MEDIA_ROOT, 'default_profiles')
    os.makedirs(default_profiles_dir, exist_ok=True)

    # Create default profile image if it doesn't exist
    default_profile_path = os.path.join(default_profiles_dir, 'default.jpg')
    if not os.path.exists(default_profile_path):
        # Create a simple default image
        try:
            from PIL import Image, ImageDraw

            # Create a 300x300 white image
            img = Image.new('RGB', (300, 300), color=(73, 109, 137))
            d = ImageDraw.Draw(img)

            # Draw a simple avatar placeholder
            d.ellipse((50, 50, 250, 250), fill=(255, 255, 255))
            d.ellipse((100, 100, 200, 200), fill=(73, 109, 137))

            img.save(default_profile_path)
        except Exception as e:
            print(f"Error creating default profile image: {e}")

    # Create default cover image if it doesn't exist
    default_cover_path = os.path.join(default_profiles_dir, 'default_cover.jpg')
    if not os.path.exists(default_cover_path):
        try:
            from PIL import Image, ImageDraw

            # Create a 1200x400 cover image with gradient
            img = Image.new('RGB', (1200, 400), color=(30, 60, 114))
            d = ImageDraw.Draw(img)

            # Draw a simple gradient
            for y in range(400):
                for x in range(1200):
                    r = int(30 + (x / 1200) * 12)
                    g = int(60 + (x / 1200) * 22)
                    b = int(114 + (x / 1200) * 30)
                    d.point((x, y), fill=(r, g, b))

            img.save(default_cover_path)
        except Exception as e:
            print(f"Error creating default cover image: {e}")
