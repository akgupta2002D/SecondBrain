from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import LifeGoal
from custom_auth.models import CustomUser

User = get_user_model()


class LifeGoalTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.life_goal = LifeGoal.objects.create(
            title='Test Goal',
            description='Test Description',
            user=self.user
        )

    def test_create_life_goal(self):
        url = reverse('lifegoal-list')
        data = {'title': 'New Goal',
                'description': 'New Description', 'user': self.user.id}
        response = self.client.post(url, data, format='json')
        print('Create LifeGoal Response:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the object was created
        created_goal = LifeGoal.objects.get(id=response.data['id'])
        self.assertEqual(created_goal.title, 'New Goal')
        self.assertEqual(created_goal.description, 'New Description')
        self.assertEqual(created_goal.user, self.user)

    def test_get_life_goal(self):
        url = reverse('lifegoal-detail', args=[self.life_goal.id])
        response = self.client.get(url, format='json')
        print('Get LifeGoal Response:', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.life_goal.title)
        self.assertEqual(
            response.data['description'], self.life_goal.description)

    def test_update_life_goal(self):
        url = reverse('lifegoal-detail', args=[self.life_goal.id])
        data = {'title': 'Updated Goal',
                'description': 'Updated Description', 'user': self.user.id}
        response = self.client.put(url, data, format='json')
        print('Update LifeGoal Response:', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.life_goal.refresh_from_db()
        self.assertEqual(self.life_goal.title, 'Updated Goal')
        self.assertEqual(self.life_goal.description, 'Updated Description')

    def test_delete_life_goal(self):
        url = reverse('lifegoal-detail', args=[self.life_goal.id])
        response = self.client.delete(url, format='json')
        print('Delete LifeGoal Response:', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the object was deleted
        with self.assertRaises(LifeGoal.DoesNotExist):
            LifeGoal.objects.get(id=self.life_goal.id)
