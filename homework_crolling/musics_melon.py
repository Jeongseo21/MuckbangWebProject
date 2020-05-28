import requests
from bs4 import BeautifulSoup             # pip install bs4

from pymongo import MongoClient           # pip install pymongo
client = MongoClient('localhost', 27017)  # mongoDB 포트번호 : 27017
db = client.dbMelonMusics                      # 'dbsparta' 생성


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.melon.com/new/index.htm',headers=headers)


soup = BeautifulSoup(data.text, 'html.parser') # 여기까지 기본세팅

melon_release = soup.select('#frm > div > table > tbody > tr')

for music in melon_release:
    m_rank = music.select_one('td > div > span.rank')
    if m_rank is not None:
        rank = m_rank.text
        #print(m_rank.text)

    m_title = music.select_one('td > div > div > div.ellipsis.rank01 > span > a') #nth-child(num)하고 붙어있는거 지워줘야함
    if m_title is not None:  #NullPointError방지
        title = m_title.text
        #print(title)
    
    m_artist = music.select_one('td > div > div > div.ellipsis.rank02 > a')
    if m_artist is not None:
        artist = m_artist.text
        # print(artist)

    doc={
        'rank': m_rank.text,
        'title': m_title.text,
        'artist': m_artist.text
    }
    db.melon_musics.insert_one(doc)

