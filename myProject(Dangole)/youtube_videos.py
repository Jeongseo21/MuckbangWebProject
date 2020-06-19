#!/usr/bin/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbproject


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyC567HkL6VbZhjGxugUXZbBJjvHalOYnsc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(q_value):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q = '이영자먹방',
    order = "date",
    part = "snippet",
    maxResults = 50
    ).execute()
  
  # print(search_response)
  videos = []
  descriptions = []
  thumbnails = []
  channelTitles = []
  publishTimes = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
      descriptions.append("%s (%s)" % (search_result["snippet"]["description"],
                                 search_result["id"]["videoId"]))
      thumbnails.append("%s (%s)" % (search_result["snippet"]["thumbnails"]["medium"],
                                   search_result["id"]["videoId"]))
      channelTitles.append("%s (%s)" % (search_result["snippet"]["channelTitle"],
                                    search_result["id"]["videoId"]))
      publishTimes.append("%s (%s)" % (search_result["snippet"]["publishTime"],
                                    search_result["id"]["videoId"]))
      




  # print("\n\nVideos:\n\n", "\n".join(videos), "\n")
  # print("\n\ndescription:\n\n", "\n".join(descriptions), "\n")
  # print("\n\nthumbnails:\n\n", "\n".join(thumbnails), "\n")
  # print("\n\nchannelTitles:\n\n", "\n".join(channelTitles), "\n")
  # print("\n\npublishTimes:\n\n", "\n".join(publishTimes), "\n")
  for i in range(0,49):
    db.myRtr.insert_one({'title':videos[i]},{'url':descriptions[i]})
    

  # for url in thumbnails :
  #   doc = {
  #      'url' : url,
  #      # 'img_url' : thumbnail,
  #      # 'channelTitle' : channel,
  #      # 'publishTime' : publishTime
  #    }
  #   db.myRtr.insert_one(doc)


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

try:
  youtube_search(args)
except HttpError as e:
  print("An HTTP error %d occurred:\n%s"% (e.resp.status, e.content))
