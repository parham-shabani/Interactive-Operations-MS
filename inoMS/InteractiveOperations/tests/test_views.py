from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from inoMS.InteractiveOperations.models import Like, Follow, Score
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class LikeViewSetTest(TestCase):
    """تست‌های ViewSet لایک"""
    
    def setUp(self):
        self.client = APIClient()
        self.like_data = {
            'actor_type': 'user',
            'actor_id': '123',
            'target_type': 'product',
            'target_id': '456',
        }
    
    def test_create_like(self):
        """تست ایجاد لایک از طریق API"""
        url = reverse('interactions:like-list')
        response = self.client.post(url, self.like_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
    
    def test_list_likes(self):
        """تست لیست کردن لایک‌ها"""
        Like.objects.create(**self.like_data)
        url = reverse('interactions:like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_like_count(self):
        """تست شمارش لایک‌ها"""
        Like.objects.create(**self.like_data)
        url = reverse('interactions:like-count', kwargs={
            'target_type': 'product',
            'target_id': '456'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes_count'], 1)



class ScoreViewSetTest(APITestCase):
    
    def setUp(self):
        self.url = reverse('interactions:score-list')
        self.valid_data = {
            'actor_type': 'user',
            'actor_id': '1',
            'target_type': 'service',
            'target_id': '10',
            'score': 3,
            'review': 'خوب بود'
        }
    
    def test_create_score(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Score.objects.count(), 1)
    
    def test_invalid_score(self):
        self.valid_data['score'] = 0  # غیرمجاز
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class FollowViewSetTest(APITestCase):

    def setUp(self):
        self.url = reverse('interactions:follow-list')
        self.data = {
            'actor_type': 'user',
            'actor_id': '1',
            'target_type': 'user',
            'target_id': '2',
        }
    
    def test_create_follow(self):
        """اولین بار فالو ارسال شود is_active=True"""
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['is_active'])
    
    def test_toggle_follow(self):
        """فالو قبلی باعث آنفالو شدن می‌شود (is_active=False)"""
        # ایجاد فالو اولیه
        self.client.post(self.url, self.data)
        # ارسال مجدد همان داده برای آنفالو
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_active'])



class ShareViewSetTest(APITestCase):
    def setUp(self):
        self.url = reverse('interactions:share-list')

    def test_create_share_in_site(self):
        data = {
            'actor_type': 'user',
            'actor_id': '1',
            'target_type': 'service',
            'target_id': '10',
            'platform': 'in_site',
            'destination_type': 'user',
            'destination_id': '2',
            'reason': 'اشتراک در سایت',
            'url': 'http://example.com/panel'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_share_telegram(self):
        data = {
            'actor_type': 'user',
            'actor_id': '1',
            'target_type': 'product',
            'target_id': '20',
            'platform': 'telegram',
            'reason': 'اشتراک در تلگرام',
            'url': 'http://example.com/product'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)