from bs4 import BeautifulSoup
import requests

"""
awards include ['Biggest gain in airplay', 'Highest ranking debut', 'Gains in performance',
                'Biggest gain in digital sales', u'Biggest gain in streams']
"""


HOT_100_URL = 'http://www.billboard.com/charts/hot-100'

def make_soup(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    return soup

def hot_100(soup):
    songs = []
    awardset = set()
    rows = soup.find_all('article', 'chart-row')
    for r in rows:
        song = dict()

        row_title = r.find('div', 'row-title')
        song['title'] = row_title.h2.text.strip()
        song['artist'] = row_title.h3.text.strip()
        try:
            song['spotify_id'] = r.select('.spotify')[0]['href'].split('track:')[-1]
        except IndexError:
            song['spotify_id'] = None
        song['history'] = r.find('div', 'row-history')['class'][1].split('-')[2]

        rankings = r.find('div', 'row-rank')
        song['this_week'] = rankings.select('.this-week')[0].text
        song['last_week'] = rankings.select('.last-week')[0].text.split(' ')[-1]

        rowstats = r.find('div', 'stats')
        stats = {}
        stats['top_spot'] = rowstats.find('div', 'stats-top-spot').find('span', 'value').text
        stats['weeks_on_chart'] = rowstats.find('div', 'stats-weeks-on-chart').find('span', 'value').text
        song['stats'] = stats

        awards = r.find('ul', 'row-awards')
        song['awards'] = [ l.text.strip() for l in awards.find_all('li') ] if awards else []

        awardset.update(song['awards'])

        songs.append(song)

    print awardset
    return songs

def main():
    soup = make_soup(HOT_100_URL)
    hot_100_list = hot_100(soup)

if __name__ == '__main__':
    main()


