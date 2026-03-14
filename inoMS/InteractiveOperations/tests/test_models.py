from django.test import TestCase
from InteractiveOperations.models import Like, Follow, Score, Share
from django.test import TestCase
from django.core.exceptions import ValidationError
from core.enums import ActorType
from InteractiveOperations.models import Share, SharePlatform


class LikeModelTest(TestCase):
    """تست‌های مدل لایک"""
    
    def setUp(self):
        self.like_data = {
            'actor_type': 'user',
            'actor_id': '123',
            'target_type': 'product',
            'target_id': '456',
        }
    
    def test_create_like(self):
        """تست ایجاد لایک"""
        like = Like.objects.create(**self.like_data)
        self.assertEqual(like.actor_type, 'user')
        self.assertEqual(like.target_type, 'product')
        self.assertIsNotNone(like.created_at)
    
    def test_like_str(self):
        """تست متد __str__"""
        like = Like.objects.create(**self.like_data)
        expected = "user:123 -> product:456"
        self.assertEqual(str(like), expected)
    
    def test_unique_constraint(self):
        """تست محدودیت یکتایی"""
        Like.objects.create(**self.like_data)
        with self.assertRaises(Exception):
            Like.objects.create(**self.like_data)


class FollowModelTest(TestCase):

    def setUp(self):
        self.follow_data = {
            'actor_type': 'user',
            'actor_id': '1',
            'target_type': 'user',
            'target_id': '2',
            'is_active': True
        }

    def test_create_follow(self):
        follow = Follow.objects.create(**self.follow_data)
        self.assertTrue(follow.is_active)
        self.assertEqual(follow.actor_type, 'user')
        self.assertEqual(follow.target_type, 'user')
    
    def test_unique_constraint(self):
        Follow.objects.create(**self.follow_data)
        with self.assertRaises(Exception):
            Follow.objects.create(**self.follow_data)




class ScoreModelTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'actor_type': 'user',
            'actor_id': '1',
            'target_type': 'service',
            'target_id': '10',
            'score': 4,
            # 'review': 'عالی بود'
        }
    
    def test_create_valid_score(self):
        score = Score.objects.create(**self.valid_data)
        self.assertEqual(score.score, 4)
    
    def test_score_validation_out_of_range(self):
        self.valid_data['score'] = 6  # خارج از محدوده
        with self.assertRaises(ValidationError):
            Score.objects.create(**self.valid_data)




class ShareModelTest(TestCase):

    def test_create_share_in_site(self):
        share = Share.objects.create(
            actor_type=ActorType.USER,
            actor_id='1',
            target_type=ActorType.SERVICE,
            target_id='10',
            platform=SharePlatform.IN_SITE,
            destination_type=ActorType.USER,
            destination_id='2',
            reason='برای تست',
            url='http://example.com/panel'
        )
        self.assertEqual(share.platform, SharePlatform.IN_SITE)
        self.assertIsNotNone(share.created_at)
        self.assertIsNotNone(share.updated_at)

    def test_create_share_external_app(self):
        share = Share.objects.create(
            actor_type=ActorType.USER,
            actor_id='1',
            target_type=ActorType.PRODUCT,
            target_id='15',
            platform=SharePlatform.TELEGRAM,
            reason='برای تست اشتراک در تلگرام',
            url='http://example.com/product'
        )
        self.assertIn(share.platform, [SharePlatform.TELEGRAM, SharePlatform.WHATSAPP])
        self.assertIsNone(share.destination_type)
        self.assertIsNone(share.destination_id)