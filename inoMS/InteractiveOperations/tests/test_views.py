# InteractiveOperations/tests/test_views.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from InteractiveOperations import enums

class FollowViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('interactive_operations:follow')
        self.valid_data = {
            "actor_type": 1, 
            "actor_id": 10, 
            "target_type": 2, 
            "target_id": 20, 
            "is_active": True
        }

    def test_follow_create_successful(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unfollow_successful(self):
        # follow
        self.client.post(self.url, self.valid_data)
        
        # unfollow
        unfollow_data = self.valid_data.copy()
        unfollow_data["is_active"] = False
        
        response = self.client.post(self.url, unfollow_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LikeViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('interactive_operations:like')
        self.like_data = {
            "actor_type": 1, 
            "actor_id": 10, 
            "target_type": 3, 
            "target_id": 15, 
            "like_status": enums.LikeStatusEnum.LIKE.value
        }

    def test_like_create_successful(self):
        response = self.client.post(self.url, self.like_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_like_direct_change_error(self):
        # like
        self.client.post(self.url, self.like_data)
        
        # change like to dislike (should raise error)
        dislike_data = self.like_data.copy()
        dislike_data["like_status"] = enums.LikeStatusEnum.DISLIKE.value
        
        response = self.client.post(self.url, dislike_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_reaction(self):
        # like
        self.client.post(self.url, self.like_data)
        
        # change like to None
        remove_data = self.like_data.copy()
        remove_data["like_status"] = enums.LikeStatusEnum.NONE.value
        
        response = self.client.post(self.url, remove_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ScoreViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('interactive_operations:score')
        self.average_url = reverse('interactive_operations:score_average')

    def test_score_invalid_range(self):
        # error score > 5
        data = {"actor_type": 1, "actor_id": 1, "target_type": 2, "target_id": 2, "score": 6}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_score_to_user(self):
        # submit score on user
        data = {"actor_type": 1, "actor_id": 1, "target_type": 1, "target_id": 2, "score": 4}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_average_score_empty(self):
        response = self.client.get(self.average_url, {"target_type": 2, "target_id": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # output == none if nothing found
        score_val = response.data.get("score") if isinstance(response.data, dict) else None
        self.assertIsNone(score_val)


class ShareViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('interactive_operations:share')

    def test_share_invalid_platform(self):
        data = {
            "actor_type": 1, "actor_id": 5, "target_type": 2, "target_id": 10,
            "platform": 99, # پلتفرم نامعتبر
            "url": "https://example.com"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_share_website_without_destination_id(self):
        data = {
            "actor_type": 1, "actor_id": 5, "target_type": 2, "target_id": 3,
            "platform": 1, "destination_id": "",
            "url": "https://daneshjoam.com"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class ListViewTests(APITestCase):
    
    def test_followers_list(self):
        url = reverse('interactive_operations:followers-list')
        response = self.client.get(url, {"target_type": 1, "target_id": 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_followings_list(self):
        url = reverse('interactive_operations:followings-list')
        response = self.client.get(url, {"actor_type": 1, "actor_id": 4})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_likers_list(self):
        url = reverse('interactive_operations:likers-list')
        response = self.client.get(url, {"target_type": 7, "target_id": 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_likees_list(self):
        url = reverse('interactive_operations:likees-list')
        response = self.client.get(url, {"actor_type": 1, "actor_id": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislikers_list(self):
        url = reverse('interactive_operations:dislikers-list')
        response = self.client.get(url, {"target_type": 3, "target_id": 120})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_dislikees_list(self):
        url = reverse('interactive_operations:dislikees-list')
        response = self.client.get(url, {"actor_type": 4, "actor_id": 23})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    