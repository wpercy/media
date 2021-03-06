from bs4 import BeautifulSoup
import requests

import traceback
import sys

"""
awards include ['Biggest gain in airplay', 'Highest ranking debut', 'Gains in performance',
                'Biggest gain in digital sales', u'Biggest gain in streams']
"""


HOT_100_URL = 'http://www.billboard.com/charts/hot-100'


class Hot100Parser(object):

    def __init__(self, url=HOT_100_URL):
        self.hot_url = url
        self.soup = self.make_soup(url)

    def make_soup(self, url):
        res = requests.get(url)
        return BeautifulSoup(res.text, 'lxml')

    def hot_100(self, soup=None):
        if soup is None:
            soup = self.soup

        songs = []
        bad_songs = []
        rows = soup.find_all('article', 'chart-row')
        for r in rows:
            song = dict()
            try:
                row_title = r.find('div', 'chart-row__title')
                song['title'] = row_title.h2.text.strip()
                # some artists aren't <a> tags so find them using next_sibling
                song['artist'] = row_title.h2.next_sibling.next_sibling.strip()
                # try:
                #     song['spotify_id'] = r.select('.spotify')[0]['href'].split('track:')[-1]
                # except IndexError:
                #     song['spotify_id'] = None
                song['history'] = r.find('div', 'chart-row__history')['class'][1].split('-')[-1]

                rankings = r.find('div', 'chart-row__rank')
                song['this_week'] = rankings.select('.chart-row__current-week')[0].text
                song['last_week'] = rankings.select('.chart-row__last-week')[0].text.split(' ')[-1]

                rowstats = r.find('div', 'chart-row__stats')
                stats = dict()
                stats['top_spot'] = rowstats.find('div', 'chart-row__top-spot').find('span', 'chart-row__value').text
                stats['weeks_on_chart'] = rowstats.find('div', 'chart-row__weeks-on-chart').find('span', 'chart-row__value').text
                song['stats'] = stats
            except AttributeError as e:
                bad_songs.append(song)

            awards = r.find('ul', 'chart-row__awards')
            song['awards'] = [l.text.strip() for l in awards.find_all('li')] if awards else []

            songs.append(song)

        return dict(songs=songs, bad=bad_songs)


def main():
    p = Hot100Parser(HOT_100_URL)
    hot_100_list = p.hot_100()
    print hot_100_list

if __name__ == '__main__':
    main()
