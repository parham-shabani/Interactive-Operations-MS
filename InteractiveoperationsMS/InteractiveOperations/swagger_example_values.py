""" *********************************** Test Api ************************************************************** """

create_instance_example_successful = {
    "data": {
        'actor_id': 23,
        "actor_type": 'User',
        "actor_ids": [1, 4, 45]
    },
    "message": "successfully created.",
    "status_code": 201,
    "errors": {},
    "success": True
}

# add for all api's
unauthorized_error_example = {
  "data": None,
  "success": False,
  "message": "Unauthorized",
  "status_code": 401,
  "errors": {}
}

# for 1n1
create_follow_example_successful = {
    "data": {
        "actor_type": 1,
        "actor_id": 1,
        "target_type": 2,
        "target_id": 2,
        "is_active": True,
    },
    "message": "user with user id 1 followed business with id 2 successfully.",
    "status_code": 200,
    "errors": {},
    "success": True,
}
create_unfollow_example_successful = {
    "data": {
       "actor_type": 1,
        "actor_id": 1,
        "target_type": 6,
        "target_id": 3,
        "is_active": False, 
    },
    "message": "user with id 1 unfollowed service with id 3 successfully.",
    "status_code": 200,
    "errors": {},
    "success": True,
}

# for 1n2, 1n3
create_like_example_successful= {
    "data": {
        "actor_type": 1,
        "actor_id": 1,
        "target_type": 7,
        "target_id": 2,
        "status": 1
    },
    "message": "user with id 1 liked comment with id 2 successfully",
    "status_code": 200,
    "errors": {},
    "success": True,
}

create_dislike_example_successful = {
    "data": {
        "actor_type": 1,
        "actor_id": 5,
        "target_type": 5,
        "target_id": 3,
        "status": 3
    },
    "message": "user with id 5 disliked product with id 3 successfully",
    "status_code": 200,
    "errors": {},
    "success": True,    
}
update_to_none_reaction_example_successful = {
    "data": {
        "actor_type": 1,
        "actor_id": 1,
        "target_type": 3,
        "target_id": 4,
        "status": 2
    },
    "message": "user with id 1 updated his reaction to industry with id 4 to 'None' successfully",
    "status_code": 200,
    "errors": {},
    "success": True,    
}
#1n4, 1n5
create_share_in_site_with_reason_example_successful = {
    "data": {
        "actor_type": 4,
        "actor_id": 1,
        "target_type": 5,
        "target_id": 2,
        "platform": 1,
        "destination_type": 3,
        "destination_id": 4,
        "url": "https://daneshjoam.com/shared-content",
        "reason": "I found this product really useful and wanted to share it with others."
    },
    "message": "business with id 1 shared product with id 2 successfully with industry with id 4 on site.",
    "status_code": 200,
    "errors": {},
    "success": True,    
}
create_share_in_site_without_reason_example_successful = {
    "data": {
        "actor_type": 1,
        "actor_id": 7,
        "target_type": 6,
        "target_id": 1,
        "platform": 1,
        "destination_type": 1,
        "destination_id": 9,
        "url": "https://daneshjoam.com/shared-content",
        "reason": ""
    },
    "message": "business with id 7 shared service with id 1 successfully with user with id 9 on site.",
    "status_code": 200,
    "errors": {},
    "success": True,
}
create_share_on_telegram_example_successful = {
    "data": {
        "actor_type": 1,
        "actor_id": 3,
        "target_type": 6,
        "target_id": 4,
        "platform": 2,
        "destination_type": None,
        "destination_id": None,
        "url": "https://daneshjoam.com/shared-service",
        "reason": ""
    },
    "message": "business with id 3 shared service with id 4 successfully with someone on telegram.",
    "status_code": 200,
    "errors": {},
    "success": True,
}
create_share_on_whatsapp_example_successful = {
    "data": {
        "actor_type": 3,
        "actor_id": 9,
        "target_type": 1,
        "target_id": 14,
        "platform": 3,
        "destination_type": None ,
        "destination_id": None,
        "url": "https://daneshjoam.com/shared-service",
        "reason": ""
    },
    "message": "industry with id 9 shared user with id 14 successfully with someone on whatsapp.",
    "status_code": 200,
    "errors": {},
    "success": True,
}
#for 1n6
create_score_example_successful ={
    "data": {
        "actor_type": 1,
        "actor_id": 1,
        "target_type": 4,
        "target_id": 2,
        "score" : 4
    },
    "message": "user with id 1 submitted score 4 on business with id 2.",
    "status_code": 200,
    "errors": {},
    "success": True,
}
# 1n7
get_average_score_example_successful = {
    "data": {
        "target_type": 4,
        "target_id": 2,
    },
    "message": "Business with id 2 has an average score of 4.5 based on 20 submitted scores.",
    "status_code": 200,
    "errors": {},
    "success": True,
}

# 1n8
get_followers_example_successful = {
    "data": {
        "target_type": 1,
        "target_id": 2,
    },
    "message": "User with id 2 has 100 followers.",
    "status_code": 200,
    "errors": {},
    "success": True,
}

# 1n9
get_followings_example_successful = {
    "data": {
        "actor_type": 1,
        "actor_id": 1,
    },
    "message": "User with id 1 is following 3 entities.",
    "status_code": 200,
    "errors": {},
    "success": True,
}

# 1n10
get_likers_example_successful = {
    "data": {
        "target_type": 7,
        "target_id": 2,
    },
    "message": "Comment with id 2 has received 150 likes.",
    "status_code": 200,
    "errors": {},
    "success": True,
}

# 1n11
get_likees_example_successful = {
    "data": {
        "actor_type": 1,
        "actor_id": 1,
    },
    "message": "User with id 1 has liked 200 entities.",
    "status_code": 200,
    "errors": {},
    "success": True,
}

# 1n12
get_dislikers_example_successful = {
    "data": {
        "target_type": 5,
        "target_id": 3,
    },
    "message": "Product with id 3 has received 100 dislikes.",
    "status_code": 200,
    "errors": {},
    "success": True,
}

# 1n13
get_dislikees_example_successful = {
    "data": {
        "actor_type": 3,
        "actor_id": 5,
    },
    "message": "Industry with id 5 has disliked 150 entities.",
    "status_code": 200,
    "errors": {},
    "success": True,
}