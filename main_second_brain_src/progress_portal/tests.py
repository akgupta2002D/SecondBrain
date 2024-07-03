from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import LifeGoal

User = get_user_model()


class LifeGoalAPITests(APITestCase):
    def setUp(self):
        # Create a user with the minimum required fields
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            firstname='Test',  # Custom field that must be set
            lastname='User'    # Custom field that must be set
        )
        self.client.login(username='testuser', password='testpassword')
        self.life_goal = LifeGoal.objects.create(
            title="Achieve Zen",
            description="Meditate daily",
            user=self.user
        )

    def test_create_life_goal(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('lifegoal-list')
        data = {'title': 'Learn Django',
                'description': 'Become proficient in Django'}
        response = self.client.post(url, data)
        print(response.data)  # To debug and confirm no other errors
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_life_goal_unauthorized(self):
        self.client.logout()  # Ensure the user is logged out
        url = reverse('lifegoal-list')
        data = {'title': 'Unauthorized Goal',
                'description': 'Should not be created'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # No new goal should be added
        self.assertEqual(LifeGoal.objects.count(), 1)

    def test_retrieve_life_goal_unauthorized(self):
        self.client.logout()
        url = reverse('lifegoal-detail', args=[self.life_goal.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_life_goal(self):
        url = reverse('lifegoal-detail', args=[self.life_goal.id])
        data = {'title': 'Updated Title',
                'description': 'Updated Description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.life_goal.refresh_from_db()
        self.assertEqual(self.life_goal.title, 'Updated Title')

    def test_update_life_goal_unauthorized(self):
        self.client.logout()
        another_user = User.objects.create_user(
            'anotheruser', 'anotherpass')
        self.client.login(username='anotheruser', password='anotherpass')
        url = reverse('lifegoal-detail', args=[self.life_goal.id])
        data = {'title': 'Unauthorized Update',
                'description': 'Attempt to update'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.life_goal.refresh_from_db()
        self.assertNotEqual(self.life_goal.title, 'Unauthorized Update')

    def test_delete_life_goal(self):
        url = reverse('lifegoal-detail', args=[self.life_goal.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(LifeGoal.objects.filter(
            id=self.life_goal.id).exists())

    def test_delete_life_goal_unauthorized(self):
        self.client.logout()
        another_user = User.objects.create_user(
            'anotheruser', 'anotherpass')
        self.client.login(username='anotheruser', password='anotherpass')
        url = reverse('lifegoal-detail', args=[self.life_goal.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(LifeGoal.objects.filter(
            id=self.life_goal.id).exists())
