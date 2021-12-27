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
import os

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
    valueA = []
    truncA = 0
    i = 0
    #data_ig = pd.DataFrame()

    for post in profile.get_posts():
        total_num_likes += post.likes
        total_num_comments += post.comments
        total_num_posts += 1

        engagement = float(total_num_likes + total_num_comments) / (num_followers * total_num_posts)
        # Integer
        # print(valueA)
        valueA.append(engagement * 100)

        # truncA = int(valueA)
        print("=" * pow(6, 2))
        print(profile.get_profile_pic_url())
        print(profile.biography)
        print("Username", profile.full_name)
        print("Verified?:", profile.is_verified)
        print("Followers:", profile.followers)
        print("Media count:", profile.mediacount)
        print("Engagement rate:", truncA, "%")
        print("Avg likes per post:", total_num_likes / total_num_posts)
        print("=" * pow(6, 2))
        urllib.request.urlretrieve(profile.get_profile_pic_url(), "C:/Users/creti/PycharmProjects/agis/analytics/static/pics/pp2.jpg")
        #img = Image.open("pp.jpg")
        picfolder = os.path.join('static', 'pics')
        flask_app.config['upload'] = picfolder
        full_filename = os.path.join(flask_app.config['upload'], 'pp2.jpg')

        # print(data_ig)

        if i == 11:
            truncA = sum(valueA)/12
            data_ig = (
                ("Username:", profile.full_name),
                ("Verified?:", profile.is_verified),
                ("Followers:", profile.followers),
                ("Media count:", profile.mediacount),
                ("Engagement rate:", ("%.1f" % truncA) + "%"),
                ("Avg likes per post:", int(total_num_likes / total_num_posts)),
                ("Bio:", profile.biography),
                ("External Url:", profile.external_url)
            )

            break

        i += 1


    data, show_data = (pd.DataFrame(),)*2
    i = 0
    for post in (posts):
        # print("out")
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
        if i == 12 :
            break

    data.index = range(1,len(data)+1) 
    # print(data.iloc[[0]])
    
    print(data)
    # show_data = data.head(12)
    
    # break



    return render_template('index.html',
                    usrname=data_ig[0][1],
                    verified=data_ig[1][1],
                    followers=(f"{data_ig[2][1]:,}"),
                    media_count=data_ig[3][1],
                    engagement_ig=data_ig[4][1],
                    avg_like=data_ig[5][1],
                    bio=data_ig[6][1],
                    url=data_ig[7][1],
                    tab_1= str(data.iloc[[0]]).replace("Link", "").replace("Dates","").replace("Likes","").replace("Comments","").replace("Views",""),
                    tab_2= str(data.iloc[[1]]).replace("Link", "").replace("Dates","").replace("Likes","").replace("Comments","").replace("Views",""),
                    tab_3= str(data.iloc[[2]]).replace("Link", "").replace("Dates","").replace("Likes","").replace("Comments","").replace("Views",""),
                    tab_4= str(data.iloc[[3]]).replace("Link", "").replace("Dates","").replace("Likes","").replace("Comments","").replace("Views",""),
                    tab_5= str(data.iloc[[4]]).replace("Link", "").replace("Dates","").replace("Likes","").replace("Comments","").replace("Views",""),
                    tab_6= str(data.iloc[[5]]).replace("Link", "").replace("Dates","").replace("Likes","").replace("Comments","").replace("Views",""),
                    tab_7= str(data.iloc[[6]]).replace("Link", "").replace("Dates","").replace("Likes","").replace("Comments","").replace("Views",""),
                    tab_8= str(data.iloc[[7]]).replace("Link", "").replace("Dates","").replace("Likes","").replace("Comments","").replace("Views",""),
                    tab_9= str(data.iloc[[8]]).replace("Link", "").replace("Dates","").replace("Likes","").replace("Comments","").replace("Views",""),
                    tab_10= str(data.iloc[[9]]).replace("Link", "").replace("Dates","").replace("Likes","").replace("Comments","").replace("Views",""),
                    tab_11= str(data.iloc[[10]]).replace("Link", "").replace("Dates","").replace("Likes","").replace("Comments","").replace("Views",""),
                    tab_12= str(data.iloc[[11]]).replace("Link", "").replace("Dates","").replace("Likes","").replace("Comments","").replace("Views",""),
                    tables=[data.to_html(classes='data', col_space = 80, justify = 'center', table_id="table")], 
                    titles=data.columns.values, 
                    user_image = full_filename)

if __name__ == "__main__":
    flask_app.run(debug=True)


# CUpWvzHhMr3
#exit()