from pymongo import MongoClient
from flask import Flask, render_template,jsonify
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

# @app.route('/list', methods=['POST'])
# def list_post():
  
#    return jsonify({'result':'success', 'msg': '이 요청은 POST!'})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

