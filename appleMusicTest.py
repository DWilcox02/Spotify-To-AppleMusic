import requests
from bs4 import BeautifulSoup
from googlesearch import search

link = "https://music.apple.com/us/album/being-so-normal/1404025195"

r = requests.get(link)
c = r.content
soup = BeautifulSoup(c, "html.parser")

with open("applemusic.html", "w") as f:
    f.write(soup.prettify())