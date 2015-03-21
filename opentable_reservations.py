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
  s = open_page(br, url)
  return _get_all_days(s)

def _get_all_days(s):
  s = s[s.index('id="NextAvailResults_ResultsGrid"'):]
  days = []

  while True:
    start = s.find('<td class="ReCol"')
    if start < 0: break
    s = s[start:]

    start = s.index('">') + 2
    end = s.index('<', start)

    date = s[start:end]
    times = _get_times(s)
    days.append((date, times))
    s = s[end:]

  return days

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
  day = datetime.datetime(2015, 3, 28, 19, 0)
  res = get_reservations(day, 281, 2)
  print 'got', len(res)
  print str(res)

  day = datetime.datetime(2015, 3, 28, 19, 0)
  res = get_reservations(day, 24433, 2)
  print 'got', len(res)
  print str(res)

  day = datetime.datetime(2015, 3, 28, 19, 0)
  res = get_reservations(day, 820, 2)
  print 'got', len(res)
  print str(res)
