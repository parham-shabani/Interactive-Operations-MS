import textwrap

# *Note: The main Swagger change log changes should be from newest to oldest, and only the last 5 should be kept.

SETTING_CHANGE_LOG = textwrap.dedent("""
### Change Log: 

### 📅 Date Of Update: 1404/12/02 
**Version:** 1.0.0  
**List of New Endpoints:**  
- `/app_name/test_api`
- `/interactive-ops/follow`
- `/interactive-ops/follow/followers/` 
- `/interactive-ops/follow/followings/` 
- `/interactive-ops/like`
- `/interactive-ops/like/likers/`
- `/interactive-ops/like/likees/`
- `/interactive-ops/like/dislikers/`
- `/interactive-ops/like/dislikees/`
- `/interactive-ops/share/`
- `/interactive-ops/score/`
- `/interactive-ops/score/average/`                                    
                                      
                                

---

### 📅 Date Of Update: 1404/../.. 
**Version:** 1.0.0  
**List of Changed Endpoints:**  
- `/..../.......`  

---

""")

# ******************************* app_name app *******************************************************************

test_api = textwrap.dedent("""
- **change operation_code to str in output**
- **fix bug display error for duplicate name in message**

""")

# ******************************* system_setting app ******************************************************************

api_name = textwrap.dedent("""
- **...........**

""")
# ******************************* report_log app **********************************************************************
