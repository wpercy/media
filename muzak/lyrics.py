from collections import defaultdict
import urllib2

from bs4 import BeautifulSoup, Comment
import requests

class Lyrics(object):

    def __init__(self):
        pass

    PRE_URL = 'http://www.azlyrics.com/lyrics/{}/{}.html'
    url = 'http://www.azlyrics.com/lyrics/johnmayer/waltgracessubmarinetestjanuary1967.html'

    def get_song_lyric_counts(self, title, artist):
        '''
        this is what you call when you want to get the actual number of lyrics
        pass in a song title and an artist
        '''
        title_string = ''.join(title.lower().split())
        artist_string = ''.join(artist.lower().split())
        song_url = self.PRE_URL.format(artist_string, title_string)
        html = urllib2.urlopen(song_url).read()
        soup = BeautifulSoup(html)
        lyric_counts = self.get_lyric_count(soup)
        return lyric_counts

    @classmethod
    def get_lyric_count(cls, soup):
        '''
        given a soup object, gets the lyrics from that soup
        '''
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


if __name__ == '__main__':
    print get_song_lyric_counts('Thunder Road', 'Bruce Springsteen')
