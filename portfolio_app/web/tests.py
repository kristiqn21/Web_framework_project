from django.contrib.auth.models import User
from django.test import TestCase, Client
from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse
from portfolio_app.auth_app.forms import RegisterUserForm, LoginUserForm
from portfolio_app.web.forms import BlogForm
from portfolio_app.web.models import Contact, Blog

UserModel = get_user_model()


class TestForms(TestCase):
    def test_login_form_widgets(self):
        form = LoginUserForm()
        self.assertIsInstance(form.fields['username'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['password'].widget, forms.PasswordInput)
        self.assertEqual(form.fields['username'].widget.attrs['class'], 'ala-bala')
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Enter your username')
        self.assertEqual(form.fields['password'].widget.attrs['class'], 'ala-bala')
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Enter your password')

    def test_register_form_widgets(self):
        form = RegisterUserForm()
        self.assertIsInstance(form.fields['username'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['email'].widget, forms.EmailInput)
        self.assertIsInstance(form.fields['password1'].widget, forms.PasswordInput)
        self.assertIsInstance(form.fields['password2'].widget, forms.PasswordInput)
        self.assertEqual(form.fields['username'].widget.attrs['class'], 'form-control')
        # Add more assertions for other widget attributes if needed

    def test_register_form_fields(self):
        form = RegisterUserForm()
        self.assertTrue('username' in form.fields)
        self.assertTrue('email' in form.fields)
        self.assertTrue('password1' in form.fields)
        self.assertTrue('password2' in form.fields)


class ContactModelTestCase(TestCase):
    def setUp(self):
        self.contact_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'This is a test message.',
        }

    def test_contact_model_creation(self):
        contact = Contact.objects.create(**self.contact_data)
        self.assertEqual(contact.name, self.contact_data['name'])
        self.assertEqual(contact.email, self.contact_data['email'])
        self.assertEqual(contact.message, self.contact_data['message'])
        self.assertIsNotNone(contact.created_at)

    def test_contact_model_str_representation(self):
        contact = Contact.objects.create(**self.contact_data)
        self.assertEqual(str(contact), self.contact_data['name'])


class BlogModelTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.blog_data = {
            'title': 'Test Blog',
            'content': 'This is a test blog post.',
            'author': self.user,
        }

    def test_blog_model_creation(self):
        blog = Blog.objects.create(**self.blog_data)
        self.assertEqual(blog.title, self.blog_data['title'])
        self.assertEqual(blog.content, self.blog_data['content'])
        self.assertEqual(blog.author, self.user)
        self.assertIsNotNone(blog.created_at)

    def test_blog_model_str_representation(self):
        blog = Blog.objects.create(**self.blog_data)
        self.assertEqual(str(blog), self.blog_data['title'])


class CreateBlogViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'testuser@example.com',
        }
        self.user = UserModel.objects.create_user(**self.user_data)

    def test_create_blog_view_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        create_blog_url = reverse('create-blog')

        # Make a POST request with valid form data
        form_data = {
            'title': 'Test Blog',
            'content': 'This is a test blog post.',
        }
        response = self.client.post(create_blog_url, form_data)

        self.assertEqual(response.status_code, 302)  # Successful form submission should redirect
        self.assertRedirects(response, reverse('blog-list'))

        # Check if the blog post is created in the database
        self.assertTrue(Blog.objects.filter(title='Test Blog', content='This is a test blog post.', author=self.user).exists())


# Add more test cases as needed for other views in your app.



