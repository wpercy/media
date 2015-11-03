from collections import defaultdict
import urllib2


from bs4 import BeautifulSoup, Comment
import requests

PRE_URL = 'http://www.azlyrics.com/lyrics/{}/{}.html'

url = 'http://www.azlyrics.com/lyrics/johnmayer/waltgracessubmarinetestjanuary1967.html'

def get_lyric_count(soup):
    comments = soup.find('div', 'ringtone').find_next_sibling("div")\
                    .find_all(text=lambda t:isinstance(t, Comment))
    [ comment.extract() for comment in comments ]

    title = soup.find('div', 'ringtone').find_next_sibling("b").text
    lyric_txt = soup.find('div', 'ringtone').find_next_sibling("div").text
    lyrics = lyric_txt.replace('\n', ' ').replace('\r', ' ').replace(',', ' ')

    counts = defaultdict(int)

    for word in lyrics.split():
        w = word.lower()
        counts[w] += 1

    # print title
    # print sorted(counts.iteritems(),key=lambda (k,v): v, reverse=True)

    return dict(title=title, lyric_counts=counts)


def get_song_lyric_counts(title, artist):
    title_string = ''.join(title.lower().split())
    artist_string = ''.join(artist.lower().split())
    song_url = PRE_URL.format(artist_string, title_string)
    html = urllib2.urlopen(song_url).read()
    soup = BeautifulSoup(html)
    lyric_counts = get_lyric_count(soup)
    return lyric_counts

if __name__ == '__main__':
    print get_song_lyric_counts('Thunder Road', 'Bruce Springsteen')
