# Generated by Django 5.0.6 on 2025-04-05 12:09

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('location', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('tweet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='tweets.tweet')),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=140)),
                ('end_date', models.DateTimeField()),
                ('tweet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='poll', to='tweets.tweet')),
            ],
        ),
        migrations.CreateModel(
            name='PollOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=140)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='tweets.poll')),
            ],
        ),
        migrations.CreateModel(
            name='PollVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_voted', models.DateTimeField(default=django.utils.timezone.now)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='tweets.polloption')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('option', 'user')},
            },
        ),
    ]
