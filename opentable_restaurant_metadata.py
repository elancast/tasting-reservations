import json
import urllib

from browser import get_browser, open_page
br = get_browser()

FIND_URL = 'http://www.opentable.com/start/httphandlers/autocompletehandler.ashx?term=%s&latitude=40.7481820&longitude=-73.9860930&MetroId=8&cuisines=true&source=startpage'
PROFILE_URL = 'http://www.opentable.com/restaurant/profile/%d'

def write_restaurant(file_name, name):
  restaurant = _find_details(name)
  if restaurant == None:
    return False
  return write_matched_restaurant(restaurant)

def write_additional_data(file_name, restaurant):
  matched = _find_details(restaurant.name, restaurant.rid)
  if matched == None:
    return False
  matched.fill_with_existing_data(restaurant)
  return write_matched_restaurant(file_name, matched)

def write_matched_restaurant(file_name, restaurant):
  restaurant.fill_additional_fields()
  restaurant.write_to_file(file_name)
  return True

def _find_details(name, id=None):
  url = FIND_URL % urllib.quote_plus(name.strip())
  s = open_page(br, url)

  doc = json.loads(s)
  matches = doc['Restaurants']
  if len(matches) == 0: return None

  match_index = _get_best_match(matches, name, id)
  if match_index < 0: return None

  return RestaurantDetails(name, matches[match_index])

def _get_best_match(matches, name, id):
  if id != None:
    return _get_match_for_id(matches, id)
  if len(matches) > 1:
    return _ask_user_for_match(name, matches)
  return -1

def _get_match_for_id(matches, id):
  for i in range(len(matches)):
    if matches[i]['Id'] == id:
      return i
  return -1

def _ask_user_for_match(name, matches):
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

    self.stars = 0
    self.price = -1
    self.cuisine = ''

  def get_handle(self):
    return self.handle_src.lower().replace(' ', '-')

  def fill_with_existing_data(self, restaurant):
    self.handle_src = restaurant.handle
    self.name = restaurant.name
    self.stars = restaurant.stars
    self.price = restaurant.price

  def fill_additional_fields(self):
    s = open_page(br, PROFILE_URL % self.rid)
    self.cuisine = self._read_itemprop(s, 'servesCuisine')

    if self.price < 0:
      price_range = self._read_itemprop(s, 'priceRange')
      dstart = price_range.rfind('$') + 1
      dend = price_range.find(' ', dstart)
      if dend < 0: dend = len(price_range)
      self.price = int(price_range[dstart:dend])

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
      str(self.stars),
      str(self.price),
      self.neighborhood,
      self.cuisine,
      ]
    f = open(file_name, 'a')
    f.write(' ~ '.join(data) + '\n')
    f.close()
