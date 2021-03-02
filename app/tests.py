from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from .models import Geolocalization
User = get_user_model()


class TestGeolocalizationViewPOSTTestCase(TestCase):
    def setUp(self):
        self.client.post('/api/register/', {'username': 'test', 'password': 'test'}, format='json')

    def test_add_new_ip_unlogged_user(self):
        response = self.client.post('/api/geolocalization/', {'address': '12.12.12.12'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_new_correct_ip_logged_user(self):
        login_response = self.client.post('/api/token/', {'username': 'test', 'password': 'test'}, format='json')
        access_token = login_response.data['access']
        token = f'Bearer {access_token}'

        ip = '12.12.12.12'
        response = self.client.post('/api/geolocalization/', {'address': ip}, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], f'IP {ip} was saved to the database.')

        response = self.client.post('/api/geolocalization/', {'address': ip}, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], f'Geolocalization with this ip ({ip}) already exists in the database.')
        db = Geolocalization.objects.filter(ip=ip)
        self.assertEqual(len(db), 1)


    def test_add_new_incorrect_ip_logged_user(self):
        login_response = self.client.post('/api/token/', {'username': 'test', 'password': 'test'}, format='json')
        access_token = login_response.data['access']
        token = f'Bearer {access_token}'

        ip = '123456789123456789'
        response = self.client.post('/api/geolocalization/', {'address': ip}, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '[Errno -2] Name or service not known. Please provide a valid IP address in body parameters.')
        db = Geolocalization.objects.filter(ip=ip)
        self.assertEqual(len(db), 0)

        ip = '12.12.12.12.12'
        response = self.client.post('/api/geolocalization/', {'address': ip}, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '[Errno -2] Name or service not known. Please provide a valid IP address in body parameters.')
        db = Geolocalization.objects.filter(ip=ip)
        self.assertEqual(len(db), 0)


class TestGeolocalizationViewGETTestCase(TestCase):
    def setUp(self):
        self.client.post('/api/register/', {'username': 'test', 'password': 'test'}, format='json')
        login_response = self.client.post('/api/token/', {'username': 'test', 'password': 'test'}, format='json')
        access_token = login_response.data['access']
        token = f'Bearer {access_token}'
        self.client.post('/api/geolocalization/', {'address': '12.12.12.12'}, format='json', HTTP_AUTHORIZATION=token)

    def test_get_ip_unlogged_user(self):
        response = self.client.get('/api/geolocalization/', {'address': '12.12.12.12'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_correct_ip_logged_user(self):
        login_response = self.client.post('/api/token/', {'username': 'test', 'password': 'test'}, format='json')
        access_token = login_response.data['access']
        token = f'Bearer {access_token}'

        ip = '12.12.12.12'
        response = self.client.get('/api/geolocalization/', {'address': ip}, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ip'], ip)
        db = Geolocalization.objects.get(ip=ip)
        self.assertEqual(db.ip, ip)


    def test_get_incorrect_ip_logged_user(self):
        login_response = self.client.post('/api/token/', {'username': 'test', 'password': 'test'}, format='json')
        access_token = login_response.data['access']
        token = f'Bearer {access_token}'

        ip = '12.12.12.12.12'
        response = self.client.get('/api/geolocalization/', {'address': ip}, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Geolocalization matching query does not exist. Please provide a valid IP address in body parameters.')
        db = Geolocalization.objects.filter(ip=ip)
        self.assertEqual(len(db), 0)

class TestGeolocalizationViewDELETETestCase(TestCase):
    def setUp(self):
        self.client.post('/api/register/', {'username': 'test', 'password': 'test'}, format='json')
        login_response = self.client.post('/api/token/', {'username': 'test', 'password': 'test'}, format='json')
        access_token = login_response.data['access']
        token = f'Bearer {access_token}'
        self.client.post('/api/geolocalization/', {'address': '12.12.12.12'}, format='json', HTTP_AUTHORIZATION=token)

    def test_delete_ip_unlogged_user(self):
        response = self.client.delete('/api/geolocalization/', {'address': '12.12.12.12'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_correct_ip_logged_user(self):
        login_response = self.client.post('/api/token/', {'username': 'test', 'password': 'test'}, format='json')
        access_token = login_response.data['access']
        token = f'Bearer {access_token}'

        ip = '12.12.12.12'
        db = Geolocalization.objects.get(ip=ip)
        self.assertEqual(db.ip, ip)
        response = self.client.delete(f'/api/geolocalization/?address={ip}', content_type='application/json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Geolocalization for IP 12.12.12.12 was removed.')
        db = Geolocalization.objects.filter(ip=ip)
        self.assertEqual(len(db), 0)

    def test_delete_incorrect_ip_logged_user(self):
        login_response = self.client.post('/api/token/', {'username': 'test', 'password': 'test'}, format='json')
        access_token = login_response.data['access']
        token = f'Bearer {access_token}'

        ip = '12.12.12.12.12'
        db = Geolocalization.objects.filter(ip=ip)
        self.assertEqual(len(db), 0)
        response = self.client.delete(f'/api/geolocalization/?address={ip}', content_type='application/json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Geolocalization matching query does not exist. Please provide a valid IP address in body parameters.')
        db = Geolocalization.objects.filter(ip=ip)
        self.assertEqual(len(db), 0)
