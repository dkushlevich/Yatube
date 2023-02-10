from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from yatube.settings import PAGE_VIEW_MULTIPLIER

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User


class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = PAGE_VIEW_MULTIPLIER

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Post.objects.filter(text__contains=query)
        else:
            return Post.objects.all()


class GroupView(ListView):
    model = Post
    template_name = 'posts/group_list.html'
    paginate_by = PAGE_VIEW_MULTIPLIER

    def get_queryset(self):
        query = self.request.GET.get('search')
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        if query:
            return group.posts.select_related('group').filter(
                text__contains=query
            )
        else:
            return group.posts.select_related('group')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(Group, slug=self.kwargs['slug'])
        return context


class FollowView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/follow.html'
    paginate_by = PAGE_VIEW_MULTIPLIER

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Post.objects.filter(text__contains=query).filter(
                author__following__user=self.request.user
            )
        else:
            return Post.objects.filter(
                author__following__user=self.request.user
            )


class ProfileView(ListView):
    model = Post
    template_name = 'posts/profile.html'
    paginate_by = PAGE_VIEW_MULTIPLIER

    def get_queryset(self):
        query = self.request.GET.get('search')
        user = get_object_or_404(User, username=self.kwargs['username'])
        if query:
            return user.posts.select_related('author').filter(
                text__contains=query
            )
        else:
            return user.posts.select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['author'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        context['count_posts'] = user.posts.count()

        context['following'] = False
        if self.request.user.is_authenticated:
            context['following'] = Follow.objects.filter(
                user=self.request.user, author=user
            )

        return context


class PostView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        context['form'] = CommentForm(self.request.POST or None,)
        context['count_posts'] = Post.objects.select_related(
            'author').filter(author=post.author).count()
        context['liked'] = post.likes.filter(id=self.request.user.id).exists()
        context['comments'] = post.comments.select_related('post')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'posts/create_post.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('posts:profile', kwargs={'username': self.request.user})

    def form_valid(self, form):
        author = Post(author=self.request.user)
        form = PostForm(
            self.request.POST,
            files=self.request.FILES,
            instance=author
        )
        form.save()
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    template_name = 'posts/create_post.html'
    form_class = PostForm
    model = Post

    def get_success_url(self):
        return reverse('posts:profile', kwargs={'username': self.request.user})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise Http404("You are not allowed to edit this Post")
        return super(PostEditView, self).dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('posts:profile', kwargs={'username': self.request.user})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user == self.object.author:
            success_url = self.get_success_url()
            self.object.delete()
            return redirect(success_url)
        return redirect('posts:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'posts/post_detail.html'
    form_class = CommentForm

    def get_object(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_success_url(self):
        return reverse(
            'posts:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = self.get_object()
        comment.save()
        return super().form_valid(form)


class AddFollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        author = User.objects.get(username=kwargs['username'])
        follow = Follow.objects.filter(user=user, author=author)
        if not follow.exists():
            try:
                Follow.objects.create(user=user, author=author)
            except IntegrityError:
                messages.error(request, 'Поздравляю! Ты нашёл паскхалку!')
            return redirect('posts:profile', username=kwargs['username'])
        return redirect('posts:profile', username=kwargs['username'])


class UnfollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        follow = get_object_or_404(
            Follow, user=request.user, author__username=self.kwargs['username']
        )
        if follow:
            follow.delete()
        return redirect('posts:profile', username=kwargs['username'])


class LikeCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=request.POST.get("comment_id"))
        post_id = comment.post.id
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        return redirect('posts:post_detail', post_id=post_id)


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=request.POST.get("post_id"))
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse(
            'posts:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user == self.object.author:
            success_url = self.get_success_url()
            self.object.delete()
            return redirect(success_url)
        return redirect('posts:index')
