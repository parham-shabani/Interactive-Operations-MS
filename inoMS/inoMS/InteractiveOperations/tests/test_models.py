from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

#changed after update models, 1405/01/15
# test nashodn. ba AI neveshte shodan


from InteractiveOperations.models.follow import UserFollowUser
class FollowModelTest(TestCase):
    def setUp(self):
        self.follow_data = {
            "actor_type": "user",
            "actor_id": "1",
            "target_type": "user",
            "target_id": "2",
            "is_active": True,
        }

    def test_create_follow(self):
        follow = UserFollowUser.objects.create(**self.follow_data)
        self.assertTrue(follow.is_active)
        self.assertEqual(follow.actor_type, "user")
        self.assertEqual(follow.target_type, "user")
        self.assertIsNotNone(follow.last_updated_at)

    def test_unique_constraint(self):
        UserFollowUser.objects.create(**self.follow_data)
        with self.assertRaises(IntegrityError):
            UserFollowUser.objects.create(**self.follow_data)


from InteractiveOperations.models.like import ServiceProviderLikeOthers
class LikeModelTest(TestCase):
    def setUp(self):
        self.like_data = {
            "actor_type": "industry",
            "actor_id": "123",
            "target_type": "comment",
            "target_id": "456",
            "is_active": True,
        }

    def test_create_like(self):
        like = ServiceProviderLikeOthers.objects.create(**self.like_data)
        self.assertEqual(like.actor_type, "user")
        self.assertEqual(like.target_type, "product")
        self.assertTrue(like.is_active)
        self.assertIsNotNone(like.last_updated_at)

    def test_unique_constraint(self):
        ServiceProviderLikeOthers.objects.create(**self.like_data)
        with self.assertRaises(IntegrityError):
            ServiceProviderLikeOthers.objects.create(**self.like_data)


from InteractiveOperations.models.score import UserScoreServiceProvider
class ScoreModelTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "actor_type": "user",
            "actor_id": "1",
            "target_type": "industry",
            "target_id": "10",
            "score": 4,
            "is_active": True,
        }

    def test_create_valid_score(self):
        score = UserScoreServiceProvider.objects.create(**self.valid_data)
        self.assertEqual(score.score, 4)
        self.assertEqual(score.target_type, "service")

    def test_score_validation_out_of_range(self):
        self.valid_data["score"] = 6
        score = UserScoreServiceProvider(**self.valid_data)
        with self.assertRaises(ValidationError):
            score.full_clean()


from InteractiveOperations.models.share import UserShareOthers, ServiceProviderShareUser
class ShareModelTest(TestCase):
    def test_create_share_in_site(self):
        share = UserShareOthers.objects.create(
            actor_type="user",
            actor_id="1",
            target_type="service",
            target_id="10",
            platform="in site",
            destination_type="user",
            destination_id="2",
            reason="برای تست",
            url="http://example.com/panel",
        )
        self.assertEqual(share.platform, "in site")
        self.assertIsNotNone(share.last_updated_at)

    def test_create_share_external_app(self):
        share = ServiceProviderShareUser.objects.create(
            actor_type="industry",
            actor_id="1",
            target_type="user",
            target_id="15",
            platform="telegram",
            destination_type=None,
            destination_id=None,
            reason="برای تست اشتراک در تلگرام",
            url="http://example.com/product",
        )
        self.assertEqual(share.platform, "telegram")
        self.assertIsNone(share.destination_type)
        self.assertIsNone(share.destination_id)
