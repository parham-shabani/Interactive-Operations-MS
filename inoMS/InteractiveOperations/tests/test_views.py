from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from InteractiveOperations.models import (
    UserFollowUser,
    UserLikeUser,
)

# test nashodn. ba AI neveshte shodan


class FollowViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.actor_id = 100
        self.target_id = 200
        self.url = reverse("follow")  # یا آدرس URL واقعی‌ات

    def test_create_new_follow(self):
        data = {
            "actor_type": "user",
            "actor_id": self.actor_id,
            "target_type": "user",
            "target_id": self.target_id,
            "is_active": True,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["is_active"], True)
        self.assertEqual(UserFollowUser.objects.count(), 1)

    def test_update_existing_follow(self):
        # ایجاد رکورد اولیه
        UserFollowUser.objects.create(
            actor_type="user",
            actor_id=self.actor_id,
            target_type="user",
            target_id=self.target_id,
            is_active=True,
        )
        data = {
            "actor_type": "user",
            "actor_id": self.actor_id,
            "target_type": "user",
            "target_id": self.target_id,
            "is_active": False,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = UserFollowUser.objects.get(
            actor_id=self.actor_id, target_id=self.target_id
        )
        self.assertFalse(obj.is_active)

    def test_follow_unsupported_combination(self):
        # از یک actor_type یا target_type پشتیبانی نشده استفاده کن
        data = {
            "actor_type": "invalid_type",
            "actor_id": 1,
            "target_type": "user",
            "target_id": 1,
            "is_active": True,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.json())


class LikeViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.actor_id = 100
        self.target_id = 200
        self.url = reverse("like")  # یا URL واقعی‌ات

    def test_create_like(self):
        data = {
            "actor_type": "user",
            "actor_id": self.actor_id,
            "target_type": "user",
            "target_id": self.target_id,
            "like_status": "like",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["like_status"], "like")
        self.assertEqual(UserLikeUser.objects.count(), 1)

    def test_change_like_to_dislike_fails(self):
        # ایجاد like اولیه
        UserLikeUser.objects.create(
            actor_type="user",
            actor_id=self.actor_id,
            target_type="user",
            target_id=self.target_id,
            like_status="like",
        )
        data = {
            "actor_type": "user",
            "actor_id": self.actor_id,
            "target_type": "user",
            "target_id": self.target_id,
            "like_status": "dislike",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.json())

    def test_remove_like(self):
        UserLikeUser.objects.create(
            actor_type="user",
            actor_id=self.actor_id,
            target_type="user",
            target_id=self.target_id,
            like_status="like",
        )
        data = {
            "actor_type": "user",
            "actor_id": self.actor_id,
            "target_type": "user",
            "target_id": self.target_id,
            "like_status": "none",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # چون like_status='none' است، احتمالاً رکورد حذف شده؛ بررسی مدل‌های خودت


class ScoreViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.actor_id = 100
        self.target_id = 200
        self.score_url = reverse("score")  # یا URL واقعی‌ات
        self.avg_url = reverse("score_average")  # یا URL واقعی‌ات

    def test_create_score(self):
        data = {
            "actor_type": "user",
            "actor_id": self.actor_id,
            "target_type": "service",
            "target_id": self.target_id,
            "score": 4,
        }
        response = self.client.post(self.score_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["score"], 4)
        self.assertEqual(UserScoreUser.objects.count(), 1)

    def test_average_score(self):
        # چند رکورد امتیاز ایجاد کن
        for score in [3, 4, 5]:
            UserScoreUser.objects.create(
                actor_type="user",
                actor_id=self.actor_id + score,
                target_type="service",
                target_id=self.target_id,
                score=score,
            )
        url = f"{self.avg_url}?target_type=service&target_id={self.target_id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertEqual(json["target_id"], self.target_id)
        self.assertGreater(json["score"], 0)
        self.assertEqual(json["count"], 3)

class ShareViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.actor_id = 100
        self.target_id = 200
        self.url = reverse("share")  # یا URL واقعی‌ات

    def test_create_share_in_site(self):
        data = {
            "actor_type": "user",
            "actor_id": self.actor_id,
            "target_type": "service",
            "target_id": self.target_id,
            "platform": "in site",
            "destination_type": "user",
            "destination_id": 2,
            "reason": "برای تست",
            "url": "http://example.com/panel",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["platform"], "in site")
        self.assertNotEqual(response.json()["created_at"], None)

    def test_create_share_external_app(self):
        data = {
            "actor_type": "user",
            "actor_id": self.actor_id,
            "target_type": "product",
            "target_id": self.target_id,
            "platform": "telegram",
            "destination_type": None,
            "destination_id": None,
            "reason": None,
            "url": "http://example.com/product",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["platform"], "telegram")
        self.assertEqual(response.json()["destination_type"], None)
        self.assertEqual(response.json()["destination_id"], None)


class FollowListViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.actor_id = 100
        self.target_id = 200
        self.followers_url = reverse("followers_list")  # یا URL واقعی‌ات
        self.followings_url = reverse("followings_list")  # یا URL واقعی‌ات
        # ایجاد چند follow فعال
        UserFollowUser.objects.create(
            actor_type="user",
            actor_id=self.actor_id,
            target_type="user",
            target_id=self.target_id,
            is_active=True,
        )

    def test_followers_list(self):
        url = f"{self.followers_url}?target_type=user&target_id={self.target_id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertEqual(json["target_id"], self.target_id)
        self.assertEqual(json["count"], 1)

    def test_followings_list(self):
        url = f"{self.followings_url}?actor_type=user&actor_id={self.actor_id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertEqual(json["actor_id"], self.actor_id)
        self.assertEqual(json["count"], 1)


class LikeListViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.actor_id = 100
        self.target_id = 200
        self.likers_url = reverse("likers_list")  # یا URL واقعی‌ات
        self.likees_url = reverse("likees_list")  # یا URL واقعی‌ات
        self.dislikers_url = reverse("dislikers_list")  # یا URL واقعی‌ات
        self.dislikees_url = reverse("dislikees_list")  # یا URL واقعی‌ات
        # ایجاد چند like
        UserLikeUser.objects.create(
            actor_type="user",
            actor_id=self.actor_id,
            target_type="user",
            target_id=self.target_id,
            like_status="like",
        )

    def test_likers_list(self):
        url = f"{self.likers_url}?target_type=user&target_id={self.target_id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertEqual(json["target_id"], self.target_id)
        self.assertEqual(json["count"], 1)

    def test_likees_list(self):
        url = f"{self.likees_url}?actor_type=user&actor_id={self.actor_id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertEqual(json["actor_id"], self.actor_id)
        self.assertEqual(json["count"], 1)

    def test_dislikers_list(self):
        UserLikeUser.objects.create(
            actor_type="user",
            actor_id=300,
            target_type="user",
            target_id=self.target_id,
            like_status="dislike",
        )
        url = f"{self.dislikers_url}?target_type=user&target_id={self.target_id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertEqual(json["count"], 1)

    def test_dislikees_list(self):
        UserLikeUser.objects.create(
            actor_type="user",
            actor_id=self.actor_id,
            target_type="user",
            target_id=300,
            like_status="dislike",
        )
        url = f"{self.dislikees_url}?actor_type=user&actor_id={self.actor_id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertEqual(json["count"], 1)


