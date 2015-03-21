
URL = 'http://www.opentable.com/%s/'

def get_restaurants_under_price(price):
  lines = _read_file()
  return filter(
    lambda restaurant: restaurant.is_under_price(price),
    map(lambda line: Restaurant(line), lines)
    )

def _read_file():
  f = open('data/michelin-prices-2.txt', 'r')
  lines = f.read().strip().split('\n')
  f.close()
  return lines

class Restaurant:
  def __init__(self, line):
    parts = line.split('|')
    self.name = parts[0]
    self.handle = parts[1]
    self.rid = int(parts[2])
    self.stars = int(parts[3])
    self.price = int(parts[4])

  def is_under_price(self, price):
    return price == None or self.price <= int(price)

  def get_url(self):
    return URL % self.handle
