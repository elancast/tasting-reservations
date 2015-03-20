from browser import get_browser, open_page

START = 'img/restimages/'
URL = 'http://www.opentable.com/%s-reservations-new-york'

br = get_browser()

f = open('data/michelin-prices.txt')
lines = f.read().strip().split('\n')
f.close()

for line in lines:
  try:
    (name, stars, price, strid) = line.split('|')
    url = URL % strid
    s = open_page(br, url)

    start = s.index(START) + len(START)
    end = s.index('.', start)
    id = s[start:end]
    print '%s|%s|%s|%s|%s' % (name, strid, id, stars, price)
  except:
    print '   -- ERROR: ', line
