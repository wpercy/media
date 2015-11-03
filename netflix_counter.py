from collections import defaultdict

shows = dict()
movies = defaultdict(list)

with open("/Users/wilbur/Downloads/recently_watched.html") as f:
    soup = BeautifulSoup(f.read())

rows = soup.find_all('li', 'retableRow')

for row in rows:
    date = row.find('div', 'date').text
    t = row.find('span', 'seriestitle')

    if t is not None: # TV Show
        try:
            showparts = [ part.strip() for part in t.parent.text.split(':') ]
            if showparts[0].lower() == showparts[1].lower():
                del showparts[1]

            if len(showparts) > 3:
                episode = ": ".join(showparts[-2:])
            else:
                episode = showparts[2]

            title, season = showparts[:2]

            season = season.split(' ')[-1]

            if title not in shows:
                shows[title] = dict()

            if season not in shows[title]:
                shows[title][season] = dict()
            if episode not in shows[title][season]:
                shows[title][season][episode] = []

            shows[title][season][episode].append(date)
        except:
            print t.parent.text

    else: # Movie
        title = row.select('.col.title')[0].text
        movies[title].append(date)

sorted_titles = sorted(shows.items(), key=operator.itemgetter(1)).reverse()
