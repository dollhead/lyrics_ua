import requests
from bs4 import BeautifulSoup
import os
import re
import sys

site_url = 'http://nashe.com.ua/'

class Song(object):
    def __init__(self, name, url):
        self.name = name
        self.url = site_url + url
    def __str__(self):
        return self.name

def get_artist_name(content):
    artist = content.find('div', 'arttitle')
    return artist.text

def get_songs(content):
    songs = []
    for s in content.find_all('a'):
        song_name = re.sub('[^\w\-_\. ]', '', s.text)
        if song_name == '':
            continue
        song = Song(song_name, s['href'])
        songs.append(song)
    return songs


def get_artist_songs(url):
    html_doc = requests.get(url).content.decode('windows-1251')
    soup = BeautifulSoup(html_doc, 'html.parser')
    content = soup.find('div', 'content')

    artist = get_artist_name(content)
    songs = get_songs(content)
    return artist, songs

def fetch_and_write_lyrics(song, artist):
    html_doc = requests.get(song.url).content.decode('windows-1251')
    soup = BeautifulSoup(html_doc, 'html.parser')
    lyrics = soup.find('div', {"id": "song2"})

    with open(artist + '\\' + song.name + '.txt', 'w', encoding='utf-8') as f:
        f.write(lyrics.text)

def fetch_lyrics(artist, songs):
    fetched, not_fetched = [], []
    if not os.path.exists(artist):
        os.makedirs(artist)

    for song in songs:
        try:
            fetch_and_write_lyrics(song, artist)
            fetched.append(song)
        except:
            print("Catched exception when fetching lyrics for " + song.name + sys.exc_info()[0])
            not_fetched.append(song)
    return fetched, not_fetched