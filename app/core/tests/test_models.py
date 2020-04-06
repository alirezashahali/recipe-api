from  django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):


    def test_create_user_with_email_successful(self):
        """test creating a user was successfull"""
        email = "ass@boobs.com"
        password = "12345"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_email_with_lowercase_URL(self):
        email = "moreass@BOOBS.com"
        password = "test12345"

        user = get_user_model().objects.create_user(email = email, password= password)

        self.assertEqual(user.email, email.lower())


    def test_email_provided(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email = None, password = '123456')

    
    def test_creating_super_user(self):
        user = get_user_model().objects.create_superuser(email = 'bitches@gmail.com', password= "123456")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)