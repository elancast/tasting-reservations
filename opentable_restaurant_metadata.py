import json
import urllib

from browser import get_browser, open_page
br = get_browser()

FIND_URL = 'http://www.opentable.com/start/httphandlers/autocompletehandler.ashx?term=%s&latitude=40.7481820&longitude=-73.9860930&MetroId=8&cuisines=true&source=startpage'
PROFILE_URL = 'http://www.opentable.com/restaurant/profile/%d'

def write_restaurant(file_name, name):
  restaurant = find_details(name)
  if restaurant == None:
    return False

  restaurant.fill_additional_fields()
  restaurant.write_to_file(file_name)
  return True

def find_details(name):
  url = FIND_URL % urllib.quote_plus(name.strip())
  s = open_page(br, url)

  doc = json.loads(s)
  matches = doc['Restaurants']
  if len(matches) == 0: return None

  match_index = 0
  if len(matches) > 1:
    match_index = ask_user_for_match(name, matches)
  if match_index < 0: return None

  return RestaurantDetails(name, matches[match_index])

def ask_user_for_match(name, matches):
  print 'Which is the best match for', name + '? Enter -1 if none match.'
  for i in range(len(matches)):
    print '%d: %s in %s' % \
        (i, matches[i]['Name'], matches[i]['Neighborhood']['Name'])

  index = None
  while index == None or index >= len(matches):
    try:
      index = int(raw_input('> '))
      if index >= len(matches):
        print 'Invalid index'
    except:
      print 'Cannot parse given index'

  print ''
  return index


class RestaurantDetails:
  def __init__(self, handle, match_json):
    self.handle_src = handle
    self.name = match_json['Name']
    self.rid = match_json['Id']
    self.neighborhood = match_json['Neighborhood']['Name']
    self.price = -1
    self.cuisine = ''

  def get_handle(self):
    return self.handle_src.lower().replace(' ', '-')

  def fill_additional_fields(self):
    s = open_page(br, PROFILE_URL % self.rid)

    price_range = self._read_itemprop(s, 'priceRange')
    dstart = price_range.rfind('$') + 1
    dend = price_range.find(' ', dstart)
    if dend < 0: dend = len(price_range)

    self.price = int(price_range[dstart:dend])
    self.cuisine = self._read_itemprop(s, 'servesCuisine')

  def _read_itemprop(self, s, prop):
    search_string = 'itemprop="%s"' % prop
    start = s.index(search_string)
    start = s.index('>', start) + 1
    end = s.index('<', start)
    return s[start:end]

  def write_to_file(self, file_name):
    data = [
      self.name,
      self.get_handle(),
      str(self.rid),
      '0',
      str(self.price),
      self.neighborhood,
      self.cuisine,
      ]
    f = open(file_name, 'a')
    f.write(' ~ '.join(data) + '\n')
    f.close()
