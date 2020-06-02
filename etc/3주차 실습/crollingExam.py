from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta 

# movie = db.movies.find_one({'title':'매트릭스'})
# print(movie['star'])

# matrics_star = movie['star']

# movies = list(db.movies.find({'star':matrics_star})) #movies라는 리스트에 매트릭스평점 영화를 다 넣음

target_movie = db.movies.find_one({'title':'매트릭스'})
target_star = target_movie['star']

db.movies.update_many({'star':target_star},{'$set':{'star':23}}) #1({조건},{변경사항})