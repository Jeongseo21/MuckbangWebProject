from pymongo import MongoClient
from flask import Flask, render_template,jsonify,request
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbproject

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/list')
def list_home():
  return render_template('list.html')

@app.route('/list/getVideo' ,methods=['GET'])
def get_videos():

  videos = list(db.HaetNim.find({},{'_id':0}))

  return jsonify({'result': 'success','videos_list':videos})

@app.route('/mypage')
def mypage_get():
  return render_template('mypage.html')

@app.route('/mypage/getContents', methods=['POST'])
def getContents():
    # 1. 클라이언트가 전달한 _give를 _receive 변수에 넣는다.
    
    restaurant_receive = request.form['restaurant_give']
    food_catg_receive = request.form['food_catg_give']
    location_receive = request.form['location_give']
    memo_receive = request.form['memo_give']

    # 2. mystar 목록에서 find_one으로 title title_receive와 일치하는 video를 찾고 리턴.
    video = db.HaetNim.find_one({'title':title_receive},{'_id':0})
    
    
    #3. db에 받아온 box contents를 저장하고 바로 리턴.
    doc = {
      'restaurant' : restaurant_receive,
      'food_catg' : food_catg_receive,
      'location' : location_receive,
      'memo' : memo_receive
    }
    db.box_contents.insert_one(doc) #insert
    contents = db.box_contents.find_one({'restrant':restaurant_receive},{'_id':0}) #find

    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success','video':video, 'contents':contents})

# @app.route('/list', methods=['POST'])
# def list_post():
  
#    return jsonify({'result':'success', 'msg': '이 요청은 POST!'})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

