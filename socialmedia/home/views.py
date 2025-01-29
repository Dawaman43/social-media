from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth import get_user_model
from .forms import ProfileForm, PostForm, SearchForm
from .models import Like, Share, UserPost, Comment, Profile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count

User = get_user_model()

# Home Page View
@login_required
def home_page(request):
    """
    Renders the homepage with posts and user details.
    """
    default_profile_pic = staticfiles_storage.url('images/default_profile.jpg')  # Default profile picture URL
    profile_picture = default_profile_pic  # Default profile picture if no user-specific image is found

    # Retrieve the posts from the database
    posts = UserPost.objects.all().order_by('-post_date')  # Fetch all posts, ordered by post date (most recent first)

    # Add the absolute URL for each post
    for post in posts:
        post.absolute_url = request.build_absolute_uri(post.get_absolute_url())  # Add the absolute URL to each post object

    # Check if the user is authenticated and handle profile picture
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)  # Get the user's profile (safe way)
        if profile and profile.profile_picture:
            profile_picture = profile.profile_picture.url  # Use the user's profile picture if available
        else:
            profile_picture = default_profile_pic  # Use default picture if profile doesn't exist

    return render(request, 'home/homepage.html', {
        'user': request.user,  # Pass the current user object to the template
        'profile_picture': profile_picture,  # Pass the user's profile picture
        'posts': posts,  # Pass the posts to the template
        'liked_posts': get_liked_posts(request.user),  # Pass the posts that the user has liked
    })

# Utility function to get liked posts
def get_liked_posts(user):
    """
    Returns a queryset of posts that the user has liked.
    """
    return UserPost.objects.filter(likes__user=user)

# Profile View by User ID
@login_required
def profile_view_by_id(request, user_id):
    """View profile by user_id."""
    user = get_object_or_404(User, id=user_id)
    return profile_view(request, user)

# Profile View by Username
@login_required
def profile_view_by_username(request, username):
    """View profile by username."""
    user = get_object_or_404(User, username=username)
    return profile_view_common(request, user)

# Profile View (for editing profile, viewing posts, etc.)
@login_required
def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = UserPost.objects.filter(user=user)  # Get posts of the specific user
    profile, created = Profile.objects.get_or_create(user=user)  # Get or create the user's profile

    is_own_profile = request.user == user  # Check if the user is viewing their own profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Save the profile form
            return redirect('user_profile', user_id=request.user.id)  # Redirect to updated profile
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'form': form,
        'profile': profile,  # Pass the profile instance to the template
        'posts': posts,  # Pass the user's posts
        'is_own_profile': is_own_profile,  # Pass a flag to indicate if it's the user's own profile
    })

# Like Post (using JsonResponse)
@login_required
def like_post(request, post_id):
    if request.method == "POST":
        post = UserPost.objects.get(id=post_id)  # Get the post by its ID
        user = request.user

        # Check if the user has already liked the post
        existing_like = Like.objects.filter(user=user, post=post).first()

        if existing_like:
            # If the user has already liked the post, remove the like
            existing_like.delete()
            is_liked = False
        else:
            # If the user has not liked the post, add the like
            Like.objects.create(user=user, post=post)
            is_liked = True

        # Update like_count dynamically
        like_count = post.likes.count()

        return JsonResponse({
            'status': 'success',
            'liked': is_liked,
            'like_count': like_count,  # Return updated like count
        })
    return JsonResponse({'status': 'error'}, status=400)

# Create a Post
@login_required
def post_content(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the current user to the post
            post.save()  # Save the post
            return redirect('home')  # Redirect to the home page
    else:
        form = PostForm()

    posts = UserPost.objects.all().order_by('-post_date')  # Fetch all posts for the homepage
    return render(request, 'home/homepage.html', {
        'form': form,
        'posts': posts,  # Pass the posts to the template
    })

# Comment on a Post
@login_required
def comment_post(request, post_id):
    post = get_object_or_404(UserPost, id=post_id)  # Get the post by its ID

    if request.method == 'POST':
        comment_content = request.POST.get('comment')  # Get the comment content from the POST request
        if comment_content:
            Comment.objects.create(user=request.user, post=post, content=comment_content)  # Create a new comment

    return redirect('home')  # Redirect back to the homepage

# Share a Post
@login_required
def share_post(request, post_id):
    post = get_object_or_404(UserPost, id=post_id)  # Get the post by its ID
    Share.objects.create(user=request.user, post=post)  # Create a new share for the post
    post.share_count = post.shares.count()  # Dynamically count shares
    post.save()  # Save the updated share count

    return JsonResponse({
        'status': 'success',
        'share_count': post.share_count  # Return updated share count
    })

# View Comments on a Post
@login_required
def post_comments_view(request, post_id):
    post = get_object_or_404(UserPost, id=post_id)  # Get the post by its ID
    comments = post.comments.all()  # Get all comments for the post

    if request.method == 'POST':
        comment_content = request.POST.get('comment')  # Get the comment content
        if comment_content:
            Comment.objects.create(user=request.user, post=post, content=comment_content)  # Create a new comment
        return redirect('post_comments', post_id=post.id)  # Redirect to the comments page

    return render(request, 'home/post_comments.html', {
        'post': post,  # Pass the post to the template
        'comments': comments,  # Pass the comments to the template
    })

# View Post Details
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(UserPost, id=post_id)  # Get the post by its ID
    comments = post.comments.all()  # Get all comments for the post

    if request.method == "POST":
        comment_content = request.POST.get("comment")  # Get the comment content
        if comment_content:
            Comment.objects.create(user=request.user, post=post, content=comment_content)  # Create a new comment
        return redirect('post_detail', post_id=post.id)  # Redirect to the post detail page

    return render(request, 'home/post_detail.html', {'post': post, 'comments': comments})  # Render the post detail page

# Edit Profile
@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile  # Get the user's profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            form.save()  # Save the profile form
            return redirect('profile', username=user.username)  # Redirect to the updated profile page
    else:
        form = ProfileForm(instance=profile, user=user)  # Pre-fill the form with current profile data

    return render(request, 'edit_profile.html', {'form': form, 'user': user})  # Render the edit profile page


# Search View
@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()  # Get the search query from the GET request
    posts = UserPost.objects.all()

    # If query is provided, filter posts by the post_text field
    if query:
        posts = posts.filter(post_text__icontains=query)

    # Sort by like count, comment count, or share count
    sort_by = request.GET.get('sort_by', 'like_count')  # Default sort is by 'like_count'

    # Annotate the posts with counts of likes, comments, and shares
    if sort_by == 'like_count':
        posts = posts.annotate(like_count_annotation=Count('likes')).order_by('-like_count_annotation')
    elif sort_by == 'comment_count':
        posts = posts.annotate(comment_count_annotation=Count('comments')).order_by('-comment_count_annotation')
    elif sort_by == 'share_count':
        posts = posts.annotate(share_count_annotation=Count('shares')).order_by('-share_count_annotation')

    # Pagination: split posts into pages, 5 posts per page
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(page)

    return render(request, 'search_results.html', {
        'page_obj': page_obj,
        'query': query,  # Pass the search query to the template
        'sort_by': sort_by,  # Pass sorting parameter to template
    })
