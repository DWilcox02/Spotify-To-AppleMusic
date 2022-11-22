import requests
from bs4 import BeautifulSoup
from googlesearch import search

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def getSpotifyInfo(link):
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    main = soup.find("div", {"id": "main"})
    
    with open("spotfy.html", "w") as f:
        f.write(main.prettify())
    
    # cover and album details
    try:
        cover = main.find("img", {"class": ["mMx2LUixlnN_Fu45JpFB","iJp40IxKg6emF6KYJ414", "CxurIfvXVb_TqGF4q8Yf", "O5_0cReFdHe81E0xFAD1"]})
        cover_image = cover["src"]
        album_name = cover["alt"]
    except:
        cover_image = ""
        album_name = ""
    
    # song title
    try:
        song_title = main.find("span", {"data-testid":"track-entity-title"}).text
    except:
        song_title = ""
    
    # song details
    try:
        song_details_html = main.find("div", {"data-testid":"track-entity-metadata"}).find_all("div", {"class": "Type__TypeElement-goli3j-0"})
        song_details = []
        for detail in song_details_html:
            song_details.append(detail.text)
        artist = song_details[0]
        year = song_details[1]
        time = song_details[2]
    except:
        artist = ""
        year = ""
        time = ""
    
    
    return {
        "title": song_title,
        "album": album_name,
        "artist": artist,
        "time": time,
        "year": year,
        "cover": cover_image
    }
    
def getSongFromAlbum(link, songInfo):
    try:
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        script = soup.find("script", {"id":"schema:music-album"}).text
        splitScript = script.split(songInfo["title"])[1]
        startingIndex = splitScript.index("https://")
        endingIndex = splitScript.index("@type") - 12
        return splitScript[startingIndex:endingIndex]
    except:
        return link

def spotifyToAppleLink(link) -> str:
    songInfo = getSpotifyInfo(link)

    # querying
    query = "music.apple.com 'song' " + songInfo["title"] + " " + songInfo["artist"] + " " + songInfo["year"]

    searchResults = []
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        searchResults.append(j)

    # check if the song is there, if so, return first result
    for result in searchResults:
        if ("music.apple.com" in link) & ("/song/" in link):
            return result
    
    # if no song, look for the album
    for result in searchResults:
        if "/album" in result:
            return getSongFromAlbum(result, songInfo)

    return ""


def appleToSpotifyLink(link):
    # heavy lifting to get spotify link
    
    newLink = "Spotify version: " + link
    return newLink