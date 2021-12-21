import math
import json
from flask import Flask, request, jsonify, render_template

import instaloader
import pandas as pd
from instaloader import Instaloader, Profile

from argparse import ArgumentParser
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect
import sys
import gc
import urllib.request
from PIL import Image

gc.collect()

import os
insta = instaloader.Instaloader()
loader = Instaloader()

try:
    from instaloader import ConnectionException, Instaloader
except ModuleNotFoundError:
    raise SystemExit("Instaloader not found.\n  pip install [--user] instaloader")


def get_cookiefile():
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("No Firefox cookies.sqlite file found. Use -c COOKIEFILE.")
    return cookiefiles[0]


def import_session(cookiefile, sessionfile):
    print("Using cookies from {}.".format(cookiefile))
    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )
    instaloader = Instaloader(max_connection_attempts=1)
    instaloader.context._session.cookies.update(cookie_data)
    username = instaloader.test_login()
    if not username:
        raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
    print("Imported session cookie for {}.".format(username))
    instaloader.context.username = username
    instaloader.save_session_to_file(sessionfile)


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("-c", "--cookiefile")
    p.add_argument("-f", "--sessionfile")
    args = p.parse_args()
    try:
        import_session(args.cookiefile or get_cookiefile(), args.sessionfile)
    except (ConnectionException, OperationalError) as e:
        raise SystemExit("Cookie import failed: {}".format(e))



flask_app = Flask(__name__)

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/analyst", methods = ["POST","GET"])
def analyst():
    # from IPython import ipapi
    # ipython = ipapi.get()
    # ipython.magic('reset -sf')
    for x in request.form.values():
        user = str(x)
    #print(link)

    target_profile = user

    profile = instaloader.Profile.from_username(loader.context, target_profile)
    # sc = loader.Po
    posts = profile.get_posts()

    num_followers = profile.followers
    total_num_likes = 0
    total_num_comments = 0
    total_num_posts = 0
    #data_ig = pd.DataFrame()

    for post in profile.get_posts():
        total_num_likes += post.likes
        total_num_comments += post.comments
        total_num_posts += 1

        engagement = float(total_num_likes + total_num_comments) / (num_followers * total_num_posts)
        # Integer
        valueA = engagement * 100
        truncA = int(valueA)
        print("=" * pow(6, 2))
        print(profile.get_profile_pic_url())
        print("Username:", profile.full_name)
        print("Verified?:", profile.is_verified)
        print("Followers:", profile.followers)
        print("Media count:", profile.mediacount)
        print("Engagement rate:", truncA, "%")
        print("Avg likes per post:", total_num_likes / total_num_posts)
        print("=" * pow(6, 2))
        urllib.request.urlretrieve(profile.get_profile_pic_url(), "pp.jpg")
        img = Image.open("pp.jpg")
        full_filename = img
        data_ig = (
            ("Url:", profile.get_profile_pic_url()),
            ("Username:",profile.full_name),
            ("Verified?:",profile.is_verified),
            ("Followers:",profile.followers),
            ("Media count:",profile.mediacount),
            ("Engagement rate:",str(truncA) + "%"),
            ("Avg likes per post:",total_num_likes / total_num_posts)
        )

        break


    data, show_data = (pd.DataFrame(),)*2
    i = 0
    for post in (posts):
        print("out")
        # x = {
        #     "link": "https://instagram.com/p/" + post.shortcode,
        #     "dates": post.date,
        #     "Likes": post.likes,
        #     "Comments": post.comments,
        #     "Views": post.video_view_count,
        # }
        data = data.append({
            "Link": "https://instagram.com/p/" + post.shortcode,
            "Dates": post.date,
            "Likes": post.likes,
            "Comments": post.comments,
            "Views": post.video_view_count
        }, ignore_index=True)
        # y = json.dumps(x, default=str)
        # if i < 5:
        #
        #     #print(x["Likes"])
        #     #print(y + ",")
        #
        # i+=1
        data = data.sort_values(['Likes'], ascending=False)

        # 12 post for the limit
        i += 1
        if i == 11 :
            break


    print(data)
    print(data.head(5))
    show_data = data.head(12)
    # break



    return render_template('index.html',data = data_ig,tables=[show_data.to_html(classes='data', index = False, col_space = 80, justify = 'center')], titles=show_data.columns.values, user_image = full_filename)

if __name__ == "__main__":
    flask_app.run(debug=True)


# CUpWvzHhMr3
#exit()