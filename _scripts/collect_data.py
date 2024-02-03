import utilities
import requests
import os
import time
import json
import copy
import pprint
from datetime import datetime, timezone


current_time = round(time.time()) # seconds
current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d') # yyyy-mm-dd
print(f"Epoch: {current_time}")
print(f"Date: {current_date}")

total_posts_filtered = 0
settings = utilities.read_file(f"/_data/settings.yml", file_type="yaml")


def get_and_update_watchlist():
  # projects example
    # [
    #   {
    #   'id': 'ethereum-magicians', 
    #   'name': 'Ethereum Magicians', 
    #   'category': 'Core', 
    #   'forum': 'https://ethereum-magicians.org/', 
    #   'propoposals_snapshot': None, 
    #   'proposals_tally': None, 
    #   'proposals_other': None, 
    #   'status': 'live', 
    #   'delegates': None
    #   }
    #   ...
    # ]
  watchlist = utilities.fetch(url="https://raw.githubusercontent.com/etheralpha/ethereumdefensealliance-com/main/_data/watchlist.yml", context="projects_watchlist", data_type="yaml")
  utilities.save_to_file(f"_data/watchlist.json", watchlist, context="projects_watchlist", data_type="json")
  # print(watchlist)
  return watchlist


def save_latest_posts(project):
  # feed types: https://meta.discourse.org/t/discourse-rss-feeds-list/264134
  if not utilities.use_test_data:
    feed_type = "latest"
    url = f"{project['forum']}/{feed_type}.rss".replace(f"//{feed_type}.rss", f"/{feed_type}.rss")
    data = utilities.fetch(url, context=f"{project['id']}", data_type="xml")
    utilities.save_to_file(f"_data/posts-raw/{project['id']}-raw.json", data, context=f"{project['id']}", data_type="json")


def add_filters(project):
  data = utilities.read_file(f"/_data/posts-raw/{project['id']}-raw.json", file_type="json")
  general = settings["general_settings"]
  # rules
    # project-specific settings are in addition to general settings
    # blacklisted category overrides whitelisted author/keyword
    # blacklisted author overrides whitelisted category/keyword
    # whitelisted author overrides blacklisted keyword
    # blacklisted keyword overrides whitelisted category
  posts_filtered = 0
  for post in data["rss"]["channel"]["item"]:
    # post example
      # {
      #   "title":"Micro oracles: a simple commitment-augmented funding mechanism",
      #   "dc:creator":"Ajesiroo",
      #   "category":"Uncategorized",
      #   "description":"<p>Just to give a bit of background. This was an idea that popped into my head when I was working on a completely unrelated, much more complicated oracle-based project. I wrote a little paper on it the following weekend, and isn\u2019t something I implemented\">Read full topic</a></p>",
      #   "link":"https://ethereum-magicians.org/t/micro-oracles-a-simple-commitment-augmented-funding-mechanism/18319",
      #   "pubDate":"Fri, 26 Jan 2024 09:04:31 +0000",
      #   "discourse:topicPinned":"No",
      #   "discourse:topicClosed":"No",
      #   "discourse:topicArchived":"No",
      #   "guid":{
      #     "@isPermaLink":"false",
      #     "#text":"ethereum-magicians.org-topic-18319"
      #   },
      #   "source":{
      #     "@url":"https://ethereum-magicians.org/t/micro-oracles-a-simple-commitment-augmented-funding-mechanism/18319.rss",
      #     "#text":"Micro oracles: a simple commitment-augmented funding mechanism"
      #   }
      # },
    proj = {
      "keyword_blacklist": [] ,
      "keyword_whitelist": [] ,
      "category_blacklist": [],
      "category_whitelist": [],
      "author_blacklist": [],
      "author_whitelist": []
    }
    if project['id'] in settings["project_settings"]:
      proj = settings["project_settings"][project['id']]
    date = post["pubDate"]
    title = post["title"]
    category = post["category"]
    author = post["dc:creator"]
    content = post["description"]
    filtered = False
    blacklisted_category = False
    blacklisted_user = False
    whitelisted_user = False
    blacklisted_keyword = False
    filter_post = False
    # blacklisted category overrides whitelisted author/keyword
    if general["category_blacklist"] and category in general["category_blacklist"]:
      blacklisted_category = True
    if proj["category_blacklist"] and category in proj["category_blacklist"]:
      blacklisted_category = True
    if proj["category_whitelist"] and category in proj["category_whitelist"]:
      blacklisted_category = False
    if blacklisted_category == True:
      filter_post = True
    else:
      # blacklisted author overrides whitelisted category/keyword
      if general["author_blacklist"] and author in general["author_blacklist"]:
        blacklisted_user = True
      if proj["author_blacklist"] and author in proj["author_blacklist"]:
        blacklisted_user = True
      if proj["author_whitelist"] and author in proj["author_whitelist"]:
        blacklisted_user = False
        whitelisted_user = True
      # whitelisted author overrides blacklisted keyword
      if blacklisted_user == True and whitelisted_user == False:
        filter_post = True
      # blacklisted keyword overrides whitelisted category
      else:
        keyword_blacklist = []
        if general["keyword_blacklist"]:
          keyword_blacklist += general["keyword_blacklist"]
        if proj["keyword_blacklist"]:
          keyword_blacklist += proj["keyword_blacklist"]
        if len(keyword_blacklist) > 0:
          for keyword in keyword_blacklist:
            if blacklisted_keyword == False:
              if keyword.casefold() in content.casefold() or keyword.casefold() in title.casefold():
                blacklisted_keyword = True
        if blacklisted_keyword == True and whitelisted_user == False:
          filter_post = True
    post["filter"] = filter_post
    if filter_post == True:
      posts_filtered += 1
    # print(f"Filtered post: {filter_post} - {post['title']}")
  if utilities.use_test_data:
    print("Save aborted, in test mode")
  else:
    utilities.save_to_file(f"_data/posts-processed/{project['id']}-processed.json", data, context=f"{project['id']}")
  print(f"Posts filtered: {posts_filtered} - {project['id']}")
  global total_posts_filtered
  total_posts_filtered += posts_filtered



def run_app():
  watchlist = get_and_update_watchlist()
  if utilities.use_test_data:
    watchlist = [watchlist[0]]
  for project in watchlist:
    if project["forum"] and project["forum_type"] == "discourse":
      save_latest_posts(project)
      add_filters(project)
  print(f"Total posts filtered: {total_posts_filtered}")



run_app()
print(f"Error count: {utilities.error_count}")




