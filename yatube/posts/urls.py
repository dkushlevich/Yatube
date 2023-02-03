from django.urls import path

from posts.views import (AddFollowView, CommentCreateView, FollowView,
                         GroupView, IndexView, LikeCommentView, LikePostView,
                         PostCreateView, PostDeleteView, PostEditView,
                         PostView, ProfileView, UnfollowView, CommentDeleteView)

app_name = 'posts'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('group/<slug:slug>/', GroupView.as_view(), name='group_list'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('posts/<int:post_id>/', PostView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path(
        'posts/delete/<int:pk>',
        PostDeleteView.as_view(),
        name='delete_post'
    ),
    path('posts/like/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path(
        'posts/like_comment/<int:comment_id>/',
        LikeCommentView.as_view(),
        name='like_comment'
    ),
    path(
        'posts/<int:post_id>/comment/',
        CommentCreateView.as_view(),
        name='add_comment'
    ),
    path('follow/', FollowView.as_view(), name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        AddFollowView.as_view(),
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        UnfollowView.as_view(),
        name='profile_unfollow'
    ),
    path(
        'comments/delete/<int:pk>',
        CommentDeleteView.as_view(),
        name='delete_comment'
    ),
]
