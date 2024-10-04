from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import *
from .forms import *


class PostsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'poster_board/posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'poster_board/post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'poster_board/post_edit.html'

    def addpage(request):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('posts')
        else:
            form = PostForm()

        return render(request, 'poster_board/post_edit.html', {'form': form})


class PostUpdate(UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'poster_board/post_edit.html'
    success_url = reverse_lazy('posts')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDelete(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'poster_board/post_delete.html'
    success_url = reverse_lazy('posts')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'poster_board/comment_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('comment_create', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        responce = form.save(commit=False)
        responce.author = self.request.user
        responce.post_id = self.kwargs['pk']
        responce.save()
        return super().form_valid(form)


class CommentDelete(UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'poster_board/comment_delete.html'
    success_url = reverse_lazy('comments')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.post.author


class CommentsList(PermissionRequiredMixin, ListView):
    permission_required = ['board.delete_comment', 'board.view_comment']
    form_class = CommentForm
    model = Comment
    template_name = 'poster_board/comments.html'
    context_object_name = 'comments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(post__author=self.request.user)
        self.filterset = CommentFilter(self.request.GET, queryset, request=self.request.user.id)
        return self.filterset.qs


class CategoryListView(ListView):
    model = Post
    template_name = 'poster_board/category_list.html'
    context_object_name = 'category_posts_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(cat=self.category).order_by('-time_create')
        return queryset


def comment_status(request, pk):
    response_objects = Comment.objects.get(pk=pk)
    response_objects.status = True
    response_objects.save()
    return redirect(reverse_lazy('comments'))


