from django.urls import path
from .views import about, index, contact_page, contact_success, blog_list, \
    create_blog, BlogDetailView, BlogDeleteView

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about page'),
    # path('blog/', blog, name='blog page'),
    path('blog/', blog_list, name='blog-list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blog/create/', create_blog, name='create-blog'),
    path('contact/', contact_page, name='contact page'),
    path('contact/success/', contact_success, name='contact_success'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),

]