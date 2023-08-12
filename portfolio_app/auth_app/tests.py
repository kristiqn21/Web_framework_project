from django.test import TestCase
from django.core import validators
from django.contrib.auth import get_user_model
from .models import PortfolioUser, validate_only_alphabetical

UserModel = get_user_model()


class PortfolioUserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'testuser@example.com',
        }

    def test_portfolio_user_creation(self):
        user = UserModel.objects.create_user(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_portfolio_user_validation(self):
            min_length = PortfolioUser.FIRST_NAME_MIN_LENGTH
            max_length = PortfolioUser.FIRST_NAME_MAX_LENGTH
            invalid_first_name = 'A' * (min_length - 1)
            valid_first_name = 'A' * max_length

            # Create a user with an invalid first_name and validate
            try:
                UserModel.objects.create_user(
                    username='testuser',
                    password='testpassword',
                    first_name=invalid_first_name,
                    email='test@example.com'
                )
                self.fail("ValidationError was not raised for invalid first_name")
            except validators.ValidationError as e:
                self.assertIn("Ensure this value has at least", str(e))

            # Create a user with an excessively long first_name and validate
            try:
                UserModel.objects.create_user(
                    username='testuser',
                    password='testpassword',
                    first_name=valid_first_name,
                    email='test@example.com'
                )
                self.fail("ValidationError was not raised for excessively long first_name")
            except validators.ValidationError as e:
                self.assertIn("Ensure this value has at most", str(e))

    def test_email_unique_validation(self):
        UserModel.objects.create_user(**self.user_data)

        # Attempt to create another user with the same email, should raise a unique constraint error
        duplicate_user_data = {
            'username': 'testuser2',
            'password': 'testpassword2',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'testuser@example.com',
        }

        with self.assertRaises(Exception):
            UserModel.objects.create_user(**duplicate_user_data)


# Add more test cases as needed for other functionality of your custom user model.
