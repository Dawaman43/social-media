
# **Social Media Platform**

A full-stack social media platform built with Django and MySQL, designed for users to interact with posts, follow others, and manage their profiles. The app includes features like secure authentication, post sharing, and social media integration (Instagram and Facebook).

---

## **Features**
- **User Authentication:** Users can register and log in using their email, username, and a secure 8-digit password.
- **Post Creation and Sharing:** Users can create posts, like, comment, and share them to Instagram and Facebook.
- **Follow System:** Users can follow and unfollow other users to view their posts in the feed.
- **Profile Management:** Users can update their profile information and profile picture, and view others' profiles.
- **Search:** Find posts by keywords or users.
- **Admin Dashboard:** Admins can manage users, including the ability to edit, delete, and deactivate accounts.

---

## **Technologies Used**
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap, jQuery, Popper
- **Database:** MySQL
- **Authentication:** Django’s built-in authentication system
- **Social Media Integration:** Facebook and Instagram sharing

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/Dawaman43/social-media.git
   ```

2. Navigate to the project directory:
   ```bash
   cd socialmedia
   ```

3. Set up the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the MySQL database:
    - Create a new database in MySQL:
      ```sql
      CREATE DATABASE social_media_db;
      ```
    - Update your `settings.py` file in Django to connect to the MySQL database:
      ```python
      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.mysql',
              'NAME' : 'socialmedia_db',
              'USER': 'django_user',
              'PASSWORD' : 'password',
              'HOST' : 'localhost',
              'PORT' : '3306'
          }
      }
      ```

6. Apply the migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

---

## **Usage**

- **Register:** Sign up using your email, username, and an 8-digit password.
- **Login:** Login to your account using your credentials.
- **Post and Engage:** Create posts, like, comment, and share them to Instagram/Facebook.
- **Profile Management:** Edit your profile and view other users’ profiles and posts.
- **Admin:** Access the admin panel to manage users and their data.

---

## **Contributing**

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make changes and commit them.
4. Push to your fork and submit a pull request.

---

## **License**

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## **Acknowledgments**

- **Django:** Powerful web framework used for the backend.
- **Bootstrap:** For responsive and modern frontend design.
- **jQuery and Popper:** For enhanced user interface interactions.
- **Social Media Sharing:** Integration with Instagram and Facebook to share posts.
