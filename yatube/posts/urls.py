from django.urls import path

from posts.views import (IndexView, add_comment, delete_post, follow_index,
                         group_posts, like_post, post_create, post_detail,
                         post_edit, profile, profile_follow, profile_unfollow, like_comment)

app_name = 'posts'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('group/<slug:slug>/', group_posts, name='group_list'),
    path('profile/<str:username>/', profile, name='profile'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('create/', post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('posts/delete/<int:post_id>', delete_post, name='delete_post'),
    path('posts/like/<int:post_id>/', like_post, name='like_post'),
    path('posts/like_comment/<int:comment_id>/', like_comment, name='like_comment'),
    path('posts/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('follow/', follow_index, name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        profile_unfollow,
        name='profile_unfollow'
    ),
]
