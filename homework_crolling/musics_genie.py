import requests
from bs4 import BeautifulSoup             # pip install bs4

from pymongo import MongoClient           # pip install pymongo
client = MongoClient('localhost', 27017)  # mongoDB 포트번호 : 27017
db = client.dbGenieMusics                      # 'dbsparta' 생성


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200403&hh=23&rtm=N&pg=1',headers=headers)


soup = BeautifulSoup(data.text, 'html.parser') # 여기까지 기본세팅


musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for music in musics:
   
    rank = music.select_one('td.number').text[0:2].strip() # [0:2] --> list의 0~2를 가져와라
    title = music.select_one('td.info > a.title.ellipsis').text.strip() # strip() --> 앞뒤 공백 제거
    singer = music.select_one('td.info > a.artist.ellipsis').text
    # print(rank,title,"/",singer)

    doc={
        'rank':rank,
        'title':title,
        'singer':singer
    }
    db.genie_musics.insert_one(doc) #딕셔너리로 만들어 db에 저장

