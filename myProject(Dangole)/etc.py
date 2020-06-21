from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbproject

videos = list(db.LeeYoungJa.find({},{'_id':0}))
print(videos)