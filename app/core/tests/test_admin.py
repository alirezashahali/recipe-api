from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTest(TestCase):


    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(email = "bitch@bitch.com", password = "123")
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = "test@bitch.com",
            password = "12345",
            name = "test user"
            )
        
    def test_users_listed(self):
        """test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """test that user edit page work"""
        url = reverse("admin:core_user_change", args = [self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """test that the create user works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)