# InteractiveOperations/tests/test_models.py
from django.test import TestCase
from InteractiveOperations.models import InteractiveRelations
from InteractiveOperations import enums

class InteractiveRelationsTests(TestCase):

    def test_normalize_actor_group_with_valid_string(self):
        self.assertEqual(InteractiveRelations._normalize_actor_group("User"), "user")
        self.assertEqual(InteractiveRelations._normalize_actor_group("Industry"), "service_provider")
        self.assertEqual(InteractiveRelations._normalize_actor_group("University"), "service_provider")
        self.assertEqual(InteractiveRelations._normalize_actor_group("Business"), "service_provider")

    def test_normalize_actor_group_with_valid_int(self):
        # base on enums
        user_int = enums.ActorTypeBase.USER.value
        industry_int = enums.ActorTypeBase.INDUSTRY.value
        university_int = enums.ActorTypeBase.UNIVERSITY.value
        business_int = enums.ActorTypeBase.BUSINESS.value
        
        self.assertEqual(InteractiveRelations._normalize_actor_group(user_int), "user")
        self.assertEqual(InteractiveRelations._normalize_actor_group(industry_int), "service_provider")
        self.assertEqual(InteractiveRelations._normalize_actor_group(university_int), "service_provider")
        self.assertEqual(InteractiveRelations._normalize_actor_group(business_int), "service_provider")


    def test_normalize_actor_group_invalid(self):
        # invalid values
        with self.assertRaises(ValueError):
            InteractiveRelations._normalize_actor_group("InvalidActor")
        with self.assertRaises(ValueError):
            InteractiveRelations._normalize_actor_group(999)



    def test_normalize_target_group_with_valid_string(self):
        self.assertEqual(InteractiveRelations._normalize_target_group("User"), "user")
        self.assertEqual(InteractiveRelations._normalize_target_group("Industry"), "service_provider")
        self.assertEqual(InteractiveRelations._normalize_target_group("University"), "service_provider")
        self.assertEqual(InteractiveRelations._normalize_target_group("Business"), "service_provider")
        self.assertEqual(InteractiveRelations._normalize_target_group("Service"), "others")
        self.assertEqual(InteractiveRelations._normalize_target_group("Product"), "others")
        self.assertEqual(InteractiveRelations._normalize_target_group("Comment"), "others")

    def test_normalize_target_group_with_valid_int(self):
        user_int = enums.TargetTypeBase.USER.value
        industry_int = enums.TargetTypeBase.INDUSTRY.value
        university_int = enums.TargetTypeBase.UNIVERSITY.value
        business_int = enums.TargetTypeBase.BUSINESS.value
        service_int = enums.TargetTypeBase.SERVICE.value
        product_int = enums.TargetTypeBase.PRODUCT.value
        comment_int = enums.TargetTypeLike.COMMENT.value

        self.assertEqual(InteractiveRelations._normalize_target_group(user_int), "user")
        self.assertEqual(InteractiveRelations._normalize_target_group(industry_int), "service_provider")
        self.assertEqual(InteractiveRelations._normalize_target_group(university_int), "service_provider")
        self.assertEqual(InteractiveRelations._normalize_target_group(business_int), "service_provider")
        self.assertEqual(InteractiveRelations._normalize_target_group(service_int), "others")
        self.assertEqual(InteractiveRelations._normalize_target_group(product_int), "others")
        self.assertEqual(InteractiveRelations._normalize_target_group(comment_int), "others")    

    def test_normalize_target_group_invalid(self):
        with self.assertRaises(ValueError):
            InteractiveRelations._normalize_target_group("UnknownTarget")
        with self.assertRaises(ValueError):
            InteractiveRelations._normalize_target_group(25)
