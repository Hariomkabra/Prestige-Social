# Prestige Social - Luxury Twitter Clone

A high-end social media platform built with Django, designed for affluent users with premium features and a sophisticated interface.

![Prestige Social](media/readme_screenshot.png)

## Features

- **Premium User Experience**
  - Elegant UI with animations and transitions
  - Sophisticated color scheme and typography
  - Interactive elements with hover effects

- **Core Social Features**
  - Post creation with rich media support
  - Like, comment, and share functionality
  - Follow/unfollow users
  - Timeline and explore feeds

- **Premium Features**
  - Advanced analytics dashboard
  - Poll creation
  - Event planning and management
  - Premium user badges

- **User Profiles**
  - Customizable profiles with cover images
  - Professional networking information
  - Activity statistics and engagement metrics

## Technology Stack

- **Backend**: Django 5.0+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production)
- **Animation Libraries**: AOS, Animate.css
- **Icons**: Font Awesome

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/prestige-social.git
   cd prestige-social
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Create dummy users (optional):
   ```
   python manage.py create_dummy_users --users 15 --tweets 8 --comments 5
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

## Deployment

### Deploying to Render

This application is configured for easy deployment on Render using the included `render.yaml` file.

1. Fork or clone this repository to your GitHub account.

2. Sign up for a [Render account](https://render.com/) if you don't have one.

3. In the Render dashboard, click on the "New +" button and select "Blueprint".

4. Connect your GitHub account and select the repository.

5. Render will automatically detect the `render.yaml` file and set up the services.

6. Click "Apply" to start the deployment process.

7. Once deployed, you can access your application at the URL provided by Render.

### Manual Deployment

You can also deploy this application manually on any Django-compatible hosting service:

1. Set the following environment variables:
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: Set to False in production
   - `ALLOWED_HOSTS`: Your domain names
   - `DATABASE_URL`: Your database connection string (if using PostgreSQL)

2. Collect static files:
   ```
   python manage.py collectstatic
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

5. Start the application using gunicorn:
   ```
   gunicorn twitter_clone.wsgi:application
   ```

## Demo Accounts

The application comes with several demo accounts that you can use to explore the features:

- Username: `abigailharris272` / Password: `password123`
- Username: `williampowell896` / Password: `password123`
- Username: `robinroberson468` / Password: `password123`
- Username: `dennisjenkins370` / Password: `password123`
- Username: `kellymccarthy823` / Password: `password123`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Bootstrap for the responsive design framework
- Font Awesome for the icons
- AOS and Animate.css for animations
- Django community for the excellent documentation and resources
