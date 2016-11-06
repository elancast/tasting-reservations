import datetime
import mechanize
import urllib

from browser import get_browser, open_request

def find_reservation_availability(dts, restaurant_ids, num_people):
  return ReservationFinder(dts, restaurant_ids, num_people).go()


COOKIES = None
def _get_cookies():
  global COOKIES
  if COOKIES != None:
    return COOKIES
  br = get_browser()
  cj = mechanize.CookieJar()
  br.set_cookiejar(cj)
  br.open('http://www.opentable.com/new-york-city-restaurants')
  COOKIES = cj
  return COOKIES


DATE_FMT = '%Y-%m-%d'
DATE_TIME_FMT = '%Y-%m-%d %H:%M'

REFERRER_URI = 'http://www.opentable.com/hakkasan-reservations-new-york?restref=%d'
REQUEST_URI = 'http://www.opentable.com/restaurant/profile/%d/search'
USER_AGENT = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'

class ReservationFinder:
  def __init__(self, dts, restaurant_ids, num_people):
    self.dts = dts
    self.restaurant_ids = restaurant_ids
    self.num_people = num_people
    self.br = get_browser()

  def go(self):
    results = {}
    for rid in self.restaurant_ids:
      results[rid] = self._go_for_restaurant(rid)
    return results

  def _go_for_restaurant(self, rid):
    results = {}
    for dt in self.dts:
      date = dt.strftime(DATE_FMT)
      if date in results:
        continue
      new_dates = self._go_for_one(rid, dt)
      for new_date in new_dates:
        results[new_date] = new_dates[new_date]
    return results

  def _go_for_one(self, rid, dt):
    print 'Searching for RID', rid, 'on', str(dt)
    request = self._get_request(rid)
    data = urllib.urlencode({
        'covers': str(self.num_people),
        'dateTime': dt.strftime(DATE_TIME_FMT),
        'restref': rid,
        })
    try:
      s = open_request(self.br, request, data)
    except:
      print 'Cannot open for ', request
      return {}
    return HTMLParser().parse(s)

  def _get_request(self, rid):
    request = mechanize.Request(REQUEST_URI % rid)
    _get_cookies().add_cookie_header(request)
    request.add_header('Referer', REFERRER_URI % rid)
    request.add_header('User-Agent', USER_AGENT)
    return request

class HTMLParser:
  def parse(self, s):
    times = self._get_all_times(s)
    results = {}
    for dt_str in times:
      (date, time) = self._get_date_and_time(dt_str)
      if not date in results:
        results[date] = []
      results[date].append(time)
    return results

  def _get_date_and_time(self, result):
    return result.split(' ')

  def _get_all_times(self, s):
    if s == None:
      return []
    (result, new_s) = self._get_next_match(s)
    results = self._get_all_times(new_s)
    if result:
      results = [result] + results
    return results

  def _get_next_match(self, s):
    start = s.find('data-datetime="')
    if start < 0:
      return (None, None)
    start += len('data-datetime="')
    end = s.find('"', start)
    return (s[start:end], s[end:])

if __name__ == '__main__':
  import datetime
  rids = [1180, 2508, 83344]
  tonight = datetime.datetime.now().replace(hour=19, minute=0, second=0, microsecond=0)
  dts = [tonight]
  results = find_reservation_availability(dts, rids, 2)
  import pdb; pdb.set_trace()
