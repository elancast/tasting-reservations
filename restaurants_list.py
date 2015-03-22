
URL = 'http://www.opentable.com/profile/%d/'

def get_restaurants_under_price(price_range):
  lines = _read_list()
  blacklist = _read_blacklist()

  results = filter(
    lambda restaurant: restaurant.is_valid(price_range, blacklist),
    map(lambda line: Restaurant(line), lines)
    )

  _warn_blacklist(blacklist)
  return results

def _warn_blacklist(blacklist):
  blacklist = filter(
    lambda i: len(i.strip()) > 0 and not i.startswith('#'),
    blacklist
    )
  if len(blacklist) > 0:
    print 'Warning: unrecognized blacklist:', ', '.join(blacklist)

def _read_blacklist():
  f = open('data/blacklist.txt', 'r')
  lines = f.read().strip().split('\n')
  f.close()
  return set(lines)

def _read_list():
  f = open('data/michelin-prices-2.txt', 'r')
  lines = f.read().strip().split('\n')
  f.close()
  return lines

class Restaurant:
  def __init__(self, line):
    parts = line.split(' ~ ')
    self.name = parts[0]
    self.handle = parts[1]
    self.rid = int(parts[2])
    self.stars = int(parts[3])
    self.price = int(parts[4])

  def is_in_price_range(self, range):
    return self.price >= range[0] and self.price <= range[1]

  def is_blacklisted(self, blacklist):
    if self.handle in blacklist:
      blacklist.remove(self.handle)
      return True
    return False

  def is_valid(self, price_range, blacklist):
    return not self.is_blacklisted(blacklist) and \
        self.is_in_price_range(price_range)

  def get_url(self):
    return URL % self.rid
