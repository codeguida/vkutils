## VkSpySystem
Allows to monitor a VK user. Current functions:
	
* Tracking user likes in his newsfeed
* Determining the age of the user, even if it is hidden

### How to use
Set depth of scanning you can by setting second argument of function **getLikes(user_id, count)**. For example:
```python
getLikes(user_id, 5) # 500 poasts
getLikes(user_id, 100) # 10 000 posts
# Small info about user
getUserInfo(user_id)
# Finding out user age
getUserAge(user_id)
```
