import os
import requests
import json
import praw
import configparser
from dotenv import load_dotenv
import time
import re
load_dotenv()

def redLogin():
      r = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            user_agent="bot by u/Mr_India_bot",
            username=os.getenv("USER_NAME"),
            password=os.getenv("PASSWORD")
            )
      return r

url = "https://safe-earth-99322.herokuapp.com/infomp/"

def runBot(r, comment_replied_to):
      for comment in r.subreddit("testingground4bots").comments(limit = 50):
            if "!mymp" in comment.body.lower() and comment.id not in comment_replied_to and comment.author != r.user.me():
                  word = ""
                  try:
                        word = re.compile("!mymp(.*)$").search(comment.body).group(1)
                  except AttributeError:
                        print("Mismatched query: !mymp <constituency name>")
                  word = word.strip().replace(" ", "%20").title()
                  res = requests.get(url + word)
                  
                  if res.status_code == 200:
                        res = json.loads(res.text)
                        comment.reply(str(res.get("constituency",{}).get("full_name",{})) + "\n\n" + str(res.get("constituency",{}).get("party",{})) + "\n\n" + str(res.get("constituency",{}).get("email_id",{})) + "\n\n" + str(res.get("constituency",{}).get("state",{}))+"\n\n&nbsp;\n\n&nbsp;"+"^^^(bleep blop)")
                        print("replied successfully")
                  else:
                        comment.reply("Not found or Mismatched query: `!mymp <constituency name>` \n\n&nbsp;\n\n&nbsp; ^^^(bleep blop)")
                        print("Replied: Not found")

                  comment_replied_to.append(comment.id)
                  with open("saved_list.txt", "a") as f:
                        f.write(comment.id + "\n")

      print("paused for 40 sec")
      time.sleep(30)

def get_saved_cmment():
      if not os.path.isfile("saved_list.txt"):
            comment_replied_to = []
      else:
            with open("saved_list.txt", "r") as f:
                  comment_replied_to = f.read()
                  comment_replied_to = comment_replied_to.split("\n")
                  # comment_replied_to = filter(None, comment_replied_to)
      return comment_replied_to


r = redLogin()
comment_replied_to = get_saved_cmment()

while True:
      runBot(r, comment_replied_to)

