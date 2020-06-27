from pymongo import MongoClient
from flask import Flask, render_template,jsonify,request
from datetime import datetime, timedelta
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbproject

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/list')
def list_home():
  return render_template('list.html')

@app.route('/mypage')
def mypage_home():
  return render_template('mypage.html')

@app.route('/mypage/getTitle', methods=['POST'])
def getTitle():
  title_receive = request.form['title_give']
  thumbnail_receive = request.form['thumbnail_give']
  videoId_receive = request.form['videoId_give']
  restaurant_receive = request.form['restaurant_give']
  food_catg_receive = request.form['food_catg_give']
  location_receive = request.form['location_give']
  memo_receive = request.form['memo_give']

  doc = {
    'title': title_receive,
    'thumbnail': thumbnail_receive,
    'videoId': videoId_receive,
    'restaurant': restaurant_receive,
    'food_catg': food_catg_receive,
    'location': location_receive,
    'memo' : memo_receive
  }
  db.mypage.insert_one(doc)
  
  return jsonify({'result':'success', 'msg':'내 보관함에 저장 완료'})

@app.route('/list/sendTitle', methods=['POST'])
def sendTitle():
  title_receive = request.form['title_give']
  
  title_one = list(db.HaetNim.find({'title':title_receive},{'_id':0}))

  return jsonify({'result':'success', 'title_one':title_one})

@app.route('/list/getVideo' ,methods=['GET'])
def get_videos():

  videos = list(db.HaetNim.find({},{'_id':0}))

  return jsonify({'result': 'success','videos_list':videos})

@app.route('/community')
def community_home():
  return render_template('community.html')

@app.route('/message', methods=['POST'])
def set_message():
  username_receive = request.form['username_give']
  contents_receive = request.form['contents_give']

  doc = {
    'username': username_receive,
    'contents': contents_receive,
    #현재 시각도 db에 저장
    'created_at': datetime.now()
  }
  db.messages.insert_one(doc)

  return jsonify({'result':'success', 'msg':'메세지 작성을 완료하였습니다.'})

@app.route('/message')
def get_messages():
  #현재 시각 구하기
  date_now = datetime.now()
  #24시간 전 구하기
  date_before = date_now - timedelta(days=1)
  messages = list(db.messages.find({'created_at':{'$gte':date_before, '$lte':date_now}},{'_id': 0}).sort('created_at',-1))

  return jsonify({'result':'success', 'messages':messages})

@app.route('/message/edit', methods=["POST"])
def edit_message():
  username_receive = request.form['username_give']
  contents_receive = request.form['contents_give']
  db.messages.update_one({'username':username_receive},
                        {'$set': {'contents':contents_receive, 'created_at':datetime.now()}})
  
  return jsonify({'result':'success', 'msg':'메세지 변경에 성공하였습니다'})


@app.route('/message/delete', methods=["POST"])
def delete_message():
  username_receive = request.form['username_give']
  
  db.messages.delete_one({'username':username_receive})
  
  return jsonify({'result':'success', 'msg':'메세지 삭제에 성공하였습니다'})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

