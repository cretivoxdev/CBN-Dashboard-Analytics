import math
import json

import instaloader
import pandas as pd
from instaloader import Instaloader, Profile
import os
insta = instaloader.Instaloader()
loader = Instaloader()

USER = "" + input('Username Login:')
PASSWORD = ""
# SHORTCODE = "" + input('Shortcode')

insta.login(USER, PASSWORD)
insta.interactive_login(USER)
insta.load_session_from_file(USER)

target_profile = "" + input('Username:')



profile = instaloader.Profile.from_username(loader.context, target_profile)
# sc = loader.Po
posts = profile.get_posts()

num_followers = profile.followers
total_num_likes = 0
total_num_comments = 0
total_num_posts = 0

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

i = 0
data = pd.DataFrame()
for post in (posts):
    # x = {
    #     "link": "https://instagram.com/p/" + post.shortcode,
    #     "dates": post.date,
    #     "Likes": post.likes,
    #     "Comments": post.comments,
    #     "Views": post.video_view_count,
    # }
    data = data.append({
        "link": "https://instagram.com/p/" + post.shortcode,
        "dates": post.date,
        "Likes": post.likes,
        "Comments": post.comments,
        "Views": post.video_view_count
    }, ignore_index=True)
    #y = json.dumps(x, default=str)
    # if i < 5:
    #
    #     #print(x["Likes"])
    #     #print(y + ",")
    #
    # i+=1
    data = data.sort_values(['Likes'], ascending=False)

print(data.sort_values(by=['Likes']).value_counts().head(3))
    # break

# CUpWvzHhMr3

exit()