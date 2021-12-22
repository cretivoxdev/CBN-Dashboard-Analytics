import math
import json
import instaloader
from datetime import datetime
from instaloader import Instaloader, Profile
insta = instaloader.Instaloader()

# 1) Login Username Session
USER = "__localhost05"
PASSWD = ""
# insta.interactive_login(USER)      # (ask password on terminal)
insta.login(USER, PASSWD)
insta.load_session_from_file(USER)
target_profile = "" + input('Username Target:')
# SHORTCODE = "" + input('Shortcode')

loader = Instaloader()




profile = instaloader.Profile.from_username(loader.context, target_profile)
posts = profile.get_posts()

num_followers = profile.followers
total_num_likes = 0
total_num_comments = 0
total_num_posts = 0

# 2) Output Profile Data
for post in profile.get_posts():
    total_num_likes += post.likes
    total_num_comments += post.comments
    total_num_posts += 1

    engagement = float (total_num_likes + total_num_comments) / (num_followers * total_num_posts)
    # Integer
    valueA = engagement * 100
    truncA = int(valueA)
    print("="*pow(6,2))
    print("Username:", profile.full_name)
    print("Verified?:", profile.is_verified)
    print("Followers:", profile.followers)
    print("Media count:", profile.mediacount)
    print("Engagement rate:", truncA, "%")
    print("Avg likes per post:", total_num_likes / total_num_posts)
    print("="*pow(6,2))
    break

# 3) Output All Posts
for post in (posts):
    x = {
        "link": "https://instagram.com/p/" + post.shortcode,
        "Date Post": post.date_local,
        "Likes": post.likes,
        "Comments": post.comments,
        "Views": post.video_view_count,
        "Hastag": post.caption_hashtags
    }
    y = json.dumps(x, indent=1, sort_keys=False, default=str, ensure_ascii=False)
    # with open('ig.json', 'w', encoding='utf-8') as f:
    print(y + ",")
    # break

# for post in (posts):
#     x = f'{{"Url": "https://instagram.com/p/{post.shortcode}", "Date": "{post.date_local}", "L":{post.likes}, "C": {post.comments}}}'
#     print(x + ",")
#     # break

# CUpWvzHhMr3

#Syutingdulu123#

exit()