from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from portfolio_app.web.forms import ContactForm, BlogForm, CommentForm, TestimonialForm
from portfolio_app.web.models import Blog, Comment, Testimonial


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def blog_list(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'blogs': blogs,
                                         'page_obj': page_obj})


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(blog=blog)
        return context


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'blog_delete.html'
    success_url = reverse_lazy('blog-list')

    def test_func(self):
        return self.request.user.is_superuser


@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog-list')
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {'form': form})


class ContactPageView(View):
    template_name = 'contact.html'
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
        return render(request, self.template_name, {'form': form})


def contact_success(request):
    return render(request, 'contact_success.html')


def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                comment=form.cleaned_data['comment'],
                blog=blog
            )
            comment.save()
            return redirect('blog-detail', pk=blog_id)
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form})


def testimonials(request):
    testimonials_data = [
        {
            'author': 'John Doe',
            'content': 'This is a great website!',
            'created_at': '2023-07-01'
        },
        {
            'author': 'Jane Smith',
            'content': 'I love the design and content.',
            'created_at': '2023-07-05'
        },
        {
            'author': 'Ivo Ivanov',
            'content': 'Good website',
            'created_at': '2023-07-05'
        },
        # Add more testimonials here...
    ]

    return render(request, 'testimonials.html', {'testimonials': testimonials_data})