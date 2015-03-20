import datetime
import urllib

from browser import get_browser, open_page

FORMAT = '%m/%d/%Y %I:%M:%S %p'
URL = 'http://www.opentable.com/opentables.aspx?m=8&p=%d&d=%s&rid=%d&t=single&scpref=0'
URL = 'http://www.opentable.com/nextavailabletable.aspx?hpu=1040606153&shpu=1&cop=1&m=8&p=%d&d=%s&rid=%d&mode=singlerest'

br = get_browser()

def get_reservations(dt, restaurant_id, people=2):
  time = urllib.quote_plus(dt.strftime(FORMAT))
  url = URL % (people, time, restaurant_id)
  print url
  s = open_page(br, url)
  return _get_times(s)

# TODO: Days
def _get_times(s):
  s = s[s.find('ResultTimes'):]
  s = s[:s.find('</ul')]
  times = []

  while True:
    start = s.find('a="')
    if start <= 0: break

    start = s.index("'", start) + 1
    end = s.index("'", start)
    dt = datetime.datetime.strptime(s[start:end], FORMAT)
    times.append(dt)
    s = s[end:]

  return times

if __name__ == '__main__':
  tomorrow = datetime.datetime(2015, 3, 21, 19, 0)
  res = get_reservations(tomorrow, 211, 2)
  print 'got', len(res)
  print str(res)

  tomorrow = datetime.datetime(2015, 3, 21, 19, 0)
  res = get_reservations(tomorrow, 24433, 2)
  print 'got', len(res)
  print str(res)
