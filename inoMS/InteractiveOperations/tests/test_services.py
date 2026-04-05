# from django.test import TestCase
# from inoMS.InteractiveOperations.models import Like, Dislike, Follow
# # from inoMS.InteractiveOperations.services.interaction_service import InteractionService


# class InteractionServiceTest(TestCase):
#     """تست‌های سرویس تعاملات"""
    
#     # def setUp(self):
#     #     self.service = InteractionService()
    
#     def test_create_like_removes_dislike(self):
#         """تست اینکه ایجاد لایک، دیسلایک قبلی رو حذف می‌کنه"""
#         # ایجاد دیسلایک
#         Dislike.objects.create(
#             actor_type='user',
#             actor_id='1',
#             target_type='product',
#             target_id='100'
#         )
        
#         # ایجاد لایک
#         self.service.create_like('user', '1', 'product', '100')
        
#         # بررسی حذف دیسلایک
#         self.assertEqual(Dislike.objects.count(), 0)
#         self.assertEqual(Like.objects.count(), 1)
    
#     def test_toggle_follow(self):
#         """تست تغییر وضعیت فالو"""
#         # اولین بار فعال میشه
#         follow = self.service.toggle_follow('user', '1', 'user', '2')
#         self.assertTrue(follow.is_active)
        
#         # دومین بار غیرفعال میشه
#         follow = self.service.toggle_follow('user', '1', 'user', '2')
#         self.assertFalse(follow.is_active)
