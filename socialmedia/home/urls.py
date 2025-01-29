from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),  # Home Page: The main entry point of the website
    path('profile/', views.profile_view, name='profile'),  # Profile Page: Displays the current user's profile
    path('edit_profile/', views.edit_profile, name='edit_profile'),  # Edit Profile Page: Allows users to edit their profile
    path('search/', views.search_view, name='search'),  # Search Page: Page to search for posts or users
    path('post/', views.post_content, name='post_content'),  # Post Content: Page for creating a new post
    path('like/<int:post_id>/', views.like_post, name='like_post'),  # Like a Post: Like a specific post based on its ID
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),  # Comment on a Post: Allows commenting on a specific post
    path('share/<int:post_id>/', views.share_post, name='share_post'),  # Share a Post: Share a post with others
    path('post/<int:post_id>/comments/', views.post_comments_view, name='post_comments'),  # View Post Comments: View all comments for a post
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # Post Detail View: Displays detailed information for a post
    path('user/<int:user_id>/profile/', views.profile_view, name='user_profile'),  # User Profile Page: Displays another user's profile
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Post Detail View: Duplicate path, consider removing
    path('like/<int:post_id>/', views.like_post, name='like_post'),  # Like a Post: Duplicate path, consider removing
]
