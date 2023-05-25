from django.test import TestCase, Client
from django.urls import reverse
from .models import Challenge, CustomUser, Solve

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', email="test@mal.com")
        self.challenge = Challenge.objects.create(name='Test Challenge', description="Test description", flag='test_flag', points=10)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_challenges_view(self):
        self.client.login(username='testuser', password='testpassword')

        # Clean up existing Solve objects
        Solve.objects.filter(user=self.user, challenge=self.challenge).delete()

        # Test with incorrect flag
        response = self.client.post(reverse('challenges'), {'flag': 'incorrect_flag'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'challenge.html')
        self.assertEqual(response.context['flag'], 'incorrect')

        # Test with correct flag
        response = self.client.post(reverse('challenges'), {'flag': 'test_flag'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'challenge.html')
        self.assertEqual(response.context['flag'], 'correct')

        # Check if Solve object already exists
        solve = Solve.objects.filter(user=self.user, challenge=self.challenge).first()
        if solve is None:
            Solve.objects.create(user=self.user, challenge=self.challenge)  # Create a Solve object to track solved challenges

        # Test with already solved challenge
        response = self.client.post(reverse('challenges'), {'flag': 'test_flag'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'challenge.html')
        self.assertEqual(response.context['flag'], 'Already solved')

    def test_scoreboard_view(self):
        response = self.client.get(reverse('scoreboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scoreboard.html')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        response = self.client.post(reverse('register'), {'username': 'newuser', 'email':'test@mail.com', 'password1': 'NewPassword@123', 'password2': 'NewPassword@123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('challenges'))

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('challenges'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))


