from flask import Flask, render_template,jsonify
import youtube_videos
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/form')
def form():
  return render_template('form.html')

@app.route('/list',methods=['GET'])
def videos():
  return render_template('list.html')

@app.route('/list',methods=['POST'])
# def videospost():
#   youtubes = youtube_videos.youtube_search()
#   print("\n\nVideos:\n\n", "\n\n".join(youtubes['videos']), "\n")
#   print("\n\nChannels:\n\n", "\n".join(youtubes['channels']), "\n")
#   print("\n\nPlaylists:\n\n", "\n".join(youtubes['playlists']), "\n")
#   return jsonify({'result':'success','videos':youtubes})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

