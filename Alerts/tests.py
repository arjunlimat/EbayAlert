from django.test import TestCase
# Create your tests here.
from rest_framework.test import APIClient
from .models import Alert

class AlertTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_alert(self):
        data = {
            'search_phrase': 'Test search',
            'email': 'test@example.com',
            'frequency': '2'
        }
        response = self.client.post('/api/alerts/create/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Alert.objects.count(), 1)

    def test_get_alert_list(self):
        response = self.client.get('/api/alerts/list/')
        self.assertEqual(response.status_code, 200)

    def test_get_alert(self):
        alert = Alert.objects.create(search_phrase='Test search', email='test@example.com', frequency='2')
        response = self.client.get(f'/api/alerts/{alert.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['search_phrase'], 'Test search')

    def test_update_alert(self):
        alert = Alert.objects.create(search_phrase='Test search', email='test@example.com', frequency='2')
        data = {
            'search_phrase': 'Updated search',
            'email': 'updated@example.com',
            'frequency': '10'
        }
        response = self.client.put(f'/api/alerts/{alert.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['search_phrase'], 'Updated search')

    def test_delete_alert(self):
        alert = Alert.objects.create(search_phrase='Test search', email='test@example.com', frequency='2')
        response = self.client.delete(f'/api/alerts/{alert.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Alert.objects.count(), 0)
