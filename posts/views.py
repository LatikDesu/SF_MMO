from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from SF_MMORPG import settings
from accounts.models import User
from posts.forms import PostForm, CommentForm
from posts.models import Post, Category, Comment


class AddComment(LoginRequiredMixin, View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Post.objects.get(id=pk)
        author = User.objects.get(id=request.user.id)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.post = post
            form.user = author
            form.save()
        return redirect(reverse('posts:post_detail', kwargs={'pk': pk}))


class AcceptComment(LoginRequiredMixin, View):

    def get(self, request, pk):
        comment = Comment.objects.get(id=pk)
        post = comment.post

        if not comment.rev_status:
            comment.rev_status = True
            comment.save()

        else:
            comment.rev_status = False
            comment.save()

        return redirect(reverse('accounts:profile', kwargs={'pk': post.user_id}))


class PostView(ListView):
    model = Post
    title = 'MMORPG - blog'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostView, self).get_context_data()
        context['title'] = self.title
        context['categoryName'] = Category.objects.filter(id=self.kwargs.get('category_id')).first()
        return context


class PostDetailView(DetailView):
    model = Post

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        context['title'] = f'{self.object.title}'
        context['author'] = User.objects.filter(pk=self.object.user_id).first()
        return context


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('post.add_post',)

    form_class = PostForm
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['TINYMCE_JS_URL'] = settings.TINYMCE_JS_URL
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)

    def form_invalid(self, form):
        invalid_fields = list(form.errors.keys())
        errors = form.errors.as_data()
        print(errors)
        print(f"Некоторые поля формы не прошли валидацию: {invalid_fields}")
        return super().form_invalid(form)


# Post update
class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('post.change_post',)

    form_class = PostForm
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.user != request.user:
            return HttpResponseForbidden("You don't have permission to edit this post.")

        return super().get(request, *args, **kwargs)


# Post delete
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('post.delete_post',)

    model = Post
    success_url = reverse_lazy('posts:post_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseForbidden("You don't have permission to delete this post.")
        return self.post(request, *args, **kwargs)
