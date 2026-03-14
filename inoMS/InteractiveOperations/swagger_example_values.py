""" *********************************** Test Api ************************************************************** """

from urllib import response


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
        "actor_type": "user",
        "actor_id": "1",
        "target_type": "business",
        "target_id": "2",
        "is_active": "True",
    },
    "message": "user with user id 1 followed business with id 2 successfully.",
    "status_code": 200,
    "errors": {},
    "success": True,
}
create_unfollow_example_successful = {
    "data": {
       "actor_type": "user",
        "actor_id": "1",
        "target_type": "service",
        "target_id": "3",
        "is_active": "False", 
    },
    "message": "user with user id 1 unfollowed service with id 3 successfully.",
    "status_code": 200,
    "errors": {},
    "success": True,
}
bad_follow_request_example = {
    "data": None,
    "success": False,
    "message": "Bad Request",
    "status_code": 400,
    "errors": {
        "actor_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business']"
        ],
        "actor_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ],
        "target_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business', 'product', 'service']"
        ],
        "target_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ],
        "is_active": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['true', 'false']"
        ]
    },
}

# for 1n2, 1n3
create_like_example_successful= {
    "data": {
        "actor_type": "user",
        "actor_id": "1",
        "target_type": "comment",
        "target_id": "2",
        "status": "like"
    },
    "message": "user with id 1 liked comment with id 2 successfully",
    "status_code": 200,
    "errors": {},
    "success": True,
}

create_dislike_example_successful = {
    "data": {
        "actor_type": "user",
        "actor_id": "5",
        "target_type": "product",
        "target_id": "3",
        "status": "dislike"
    },
    "message": "user with id 5 disliked product with id 3 successfully",
    "status_code": 200,
    "errors": {},
    "success": True,    
}
update_to_none_reaction_example_successful = {
    "data": {
        "actor_type": "user",
        "actor_id": "1",
        "target_type": "industry",
        "target_id": "4",
        "status": "none"
    },
    "message": "user with id 1 updated his reaction to industry with id 4 to 'None' successfully",
    "status_code": 200,
    "errors": {},
    "success": True,    
}
bad_like_request_example = {
    "data": None,
    "success": False,
    "message": "Bad Request",
    "status_code": 400,
    "errors": {
        "actor_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business']",
        ],
        "actor_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ],
        "target_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business', 'product', 'service', 'comment']"
        ],
        "target_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ],
        "like_status": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['like', 'dislike', 'none']"
        ]
    },
}

#1n4, 1n5
create_share_in_site_with_reason_example_successful = {
    "data": {
        "actor_type": "business",
        "actor_id": "1",
        "target_type": "product",
        "target_id": "2",
        "platform": "in_site",
        "destination_type": "industry",
        "destination_id": "4",
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
        "actor_type": "user",
        "actor_id": "7",
        "target_type": "service",
        "target_id": "1",
        "platform": "in_site",
        "destination_type": "user",
        "destination_id": "9",
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
        "actor_type": "user",
        "actor_id": "3",
        "target_type": "service",
        "target_id": "4",
        "platform": "telegram",
        "destination_type": "",
        "destination_id": "",
        "url": "https://daneshjoam.com/shared-service",
        "reason": "This service is excellent for our needs, highly recommended!"
    },
    "message": "business with id 3 shared service with id 4 successfully with someone on telegram.",
    "status_code": 200,
    "errors": {},
    "success": True,
}
create_share_on_whatsapp_example_successful = {
    "data": {
        "actor_type": "industry",
        "actor_id": "9",
        "target_type": "user",
        "target_id": "14",
        "platform": "whatsapp",
        "destination_type": "",
        "destination_id": "",
        "url": "https://daneshjoam.com/shared-service",
        "reason": "This service is excellent for our needs, highly recommended!"
    },
    "message": "industry with id 9 shared user with id 14 successfully with someone on whatsapp.",
    "status_code": 200,
    "errors": {},
    "success": True,
}
bad_create_share_request_example = {
    "data": None,
    "success": False,
    "message": "Bad Request",
    "status_code": 400,
    "errors": {
        "actor_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business']"
        ],
        "actor_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ],
        "target_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business', 'product', 'service']"
        ],
        "target_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ],
        "platform": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['in_site', 'telegram', 'whatsapp']"
        ],
        "destination_type": [
            "این فیلد در صورتی که پلتفرم سایت نباشد باید خالی بماند"
            "در صورتی که پلتفرم سایت باشد این فیلد باید از بین موارد زیر باید انتخاب شود"
            "['user', 'university', 'industry', 'business']"
        ],
        "destination_id": [
            "این فیلد در صورتی که پلتفرم سایت نباشد باید خالی بماند"
            "در صورتی که پلتفرم سایت باشد این فیلد باید یک عدد مثبت باشد"
        ],
        "url": [
            "این فیلد اختیاری است و باید یک URL معتبر باشد."
        ]
    },
}

#for 1n6

create_score_example_successful ={
    "data": {
        "actor_type": "user",
        "actor_id": "1",
        "target_type": "business",
        "target_id": "2",
        "score" : "4"
    },
    "message": "user with id 1 submitted score 4 on business with id 2.",
    "status_code": 200,
    "errors": {},
    "success": True,
}
bad_create_score_request_example = {
    "data": None,
    "success": False,
    "message": "Bad Request",
    "status_code": 400,
    "errors": {
        "actor_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business']"
        ],
        "actor_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ],
        "target_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['university', 'industry', 'business', 'product', 'service']"
        ],
        "target_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ],
        "score": [
            "این فیلد الزامی است و باید یک عدد بین 1 تا 5 باشد."
        ]
    },
}

#1n7
get_average_score_example_successful = {
    "data": {
        "target_type": "business",
        "target_id": "2",
    },
    "message": {
        "target_type": "business",
        "target_id": "2",
        "average_score": 4.5,
        "count": 20,
    },
    "status_code": 200,
    "errors": {},
    "success": True,
}
bad_get_average_score_request_example = {
    "data": None,
    "success": False,
    "message": "Bad Request",
    "status_code": 400,
    "errors": {
        "target_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['university', 'industry', 'business', 'product', 'service']"
        ],
        "target_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ]
    },
}

#1n8
get_followers_example_successful = {
    "data": {
        "target_type": "user",
        "target_id": "2",
    },
    "message": {
        "target_type": "user",
        "target_id": "2",
        "count": 100,
        "results": [
            {"actor_type": "user", "actor_id": 1},
            {"actor_type": "business", "actor_id": 3},
            {"actor_type": "individual", "actor_id": 5},
            # ... more followers
        ]
    },
    "status_code": 200,
    "errors": {},
    "success": True,
}
bad_get_followers_request_example = {
    "data": None,
    "success": False,
    "message": "Bad Request",
    "status_code": 400,
    "errors": {
        "target_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business', 'product', 'service']"
        ],
        "target_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ]
    },
}

#1n9    
get_followings_example_successful = {
    "data": {
        "actor_type": "user",
        "actor_id": "1",    
    },
    "message": {
        "actor_type": "user",
        "actor_id": "1",
        "count": 3,
        "results": [
            {"target_type": "user", "target_id": 2},
            {"target_type": "business", "target_id": 4},
            {"target_type": "industry", "target_id": 5},
            # ... more followings
        ]
    },
    "status_code": 200,
    "errors": {},
    "success": True,
}
bad_get_followings_request_example = {
    "data": None,
    "success": False,
    "message": "Bad Request",
    "status_code": 400,
    "errors": {
        "actor_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business']"
        ],
        "actor_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ]
    },
}

#1n10
get_likers_example_successful = {
    "data": {
        "target_type": "comment",
        "target_id": "2",
    },
    "message": {
        "target_type": "comment",
        "target_id": "2",
        "count": 150,
        "results": [
            {"actor_type": "user", "actor_id": 1},
            {"actor_type": "business", "actor_id": 3},
            {"actor_type": "individual", "actor_id": 5},
            # ... more likers
        ]
    },
    "status_code": 200,
    "errors": {},
    "success": True,
}
bad_get_likers_request_example = {
    "data": None,
    "success": False,
    "message": "Bad Request",
    "status_code": 400,
    "errors": {
        "target_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business', 'product', 'service', 'comment']"
        ],
        "target_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ]
    },
}

#1n11
get_likees_example_successful = {
    "data": {
        "actor_type": "user",
        "actor_id": "1",
    },
    "message": {
        "actor_type": "user",
        "actor_id": "1",
        "count": 200,
        "results": [
            {"target_type": "comment", "target_id": 2},
            {"target_type": "product", "target_id": 3},
            {"target_type": "service", "target_id": 4},
            # ... more likees
        ]
    },
    "status_code": 200,
    "errors": {},
    "success": True,
}
bad_get_likees_request_example = {
    "data": None,
    "success": False,
    "message": "Bad Request",
    "status_code": 400,
    "errors": {
        "actor_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business']"
        ],
        "actor_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ]
    },
}

#1n12
get_dislikers_example_successful = {
    "data": {
        "target_type": "product",
        "target_id": "3",
    },
    "message": {
        "target_type": "product",
        "target_id": "3",
        "count": 100,
        "results": [
            {"actor_type": "user", "actor_id": 1},
            {"actor_type": "business", "actor_id": 2},
            {"actor_type": "individual", "actor_id": 4},
            # ... more dislikers
        ]
    },
    "status_code": 200,
    "errors": {},
    "success": True,
}
bad_get_dislikers_request_example = {
    "data": None,
    "success": False,
    "message": "Bad Request",
    "status_code": 400,
    "errors": {
        "target_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business', 'product', 'service', 'comment']"
        ],
        "target_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ]
    },
}

#1n13
get_dislikees_example_successful = {
    "data": {
        "actor_type": "industry",
        "actor_id": "5",
    },
    "message": {
        "actor_type": "user",
        "actor_id": "5",
        "count": 150,
        "results": [
            {"target_type": "product", "target_id": 1},
            {"target_type": "service", "target_id": 2},
            {"target_type": "comment", "target_id": 3},
            # ... more dislikees
        ]
    },
    "status_code": 200,
    "errors": {},
    "success": True,
}
bad_get_dislikees_request_example = {
    "data": None,
    "success": False,
    "message": "Bad Request",
    "status_code": 400,
    "errors": {
        "actor_type": [
            "این فیلد الزامی است و باید یکی از مقادیر زیر باشد.",
            "['user', 'university', 'industry', 'business']"
        ],
        "actor_id": [
            "این فیلد الزامی است و باید یک عدد مثبت باشد"
        ]
    },
}