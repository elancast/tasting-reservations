from termcolor import colored

CUISINE_LEN = 22
NAME_LEN = 20
NEIGHBORHOOD_LEN = 20
MAX_RESERVATIONS = 6
TIME_LEN = 7

COLORED_PHRASES = {
  'East Village': 'green',
  'Upper East Side': 'green',
  'Sushi': 'green',

  'Greenwich Village': 'yellow',
  'Midtown East': 'yellow',
  'Murray Hill': 'yellow',
  'Union Square': 'yellow',
  }

def print_reservations(days, restaurants, reservations):
  printer = ReservationPrinter(restaurants, reservations)
  map(lambda day: printer.print_day(day), sorted(days))

class ReservationPrinter:
  def __init__(self, restaurants, reservations):
    # Index restaurants by their ID
    self._restaurants = {}
    for restaurant in restaurants:
      self._restaurants[restaurant.rid] = restaurant

    # Index reservations by date, then by restaurant ID
    self._reservations = {}
    for rid in reservations:
      for (date, r_list) in reservations[rid]:
        if not date in self._reservations:
          self._reservations[date] = {}
        self._reservations[date][rid] = r_list

  def print_day(self, day):
    print day.strftime('%a, %b %d')

    restaurants = \
        {} if not day in self._reservations else self._reservations[day]
    if len(restaurants) == 0:
      print '  No reservations found.'

    # Sort restaurants by optimal output ordering and then print!
    ordered_rids = sorted(
      restaurants.keys(),
      key=lambda rid: self._get_sort(self._restaurants[rid])
      )
    for rid in ordered_rids:
      self._print_restaurant_reservations(rid, restaurants[rid])

    print ''

  def _get_sort(self, restaurant):
    return (restaurant.price, restaurant.name.lower())

  def _print_restaurant_reservations(self, rid, reservations):
    if len(reservations) == 0: return

    restaurant = self._restaurants[rid]
    stars_text = ''.join(['*' for i in range(restaurant.stars)])
    price_text = self._pad_len('(%d)' % restaurant.price, 5)

    # **  (price) Name         <times>  <neighborhood> <cuisine>  <url>
    print self._pad_len(stars_text, 3),
    print price_text,
    print self._pad_len(restaurant.name, NAME_LEN),
    print self._pad_len('', 6),

    times = ''.join(map(
      lambda dt: self._stringitize_reservation(dt),
      reservations
      ))
    print self._pad_len(times, TIME_LEN * MAX_RESERVATIONS),

    print self._pad_len(restaurant.neighborhood, NEIGHBORHOOD_LEN), '',
    print self._pad_len(restaurant.cuisine, CUISINE_LEN), '',

    print restaurant.get_url(),
    print ''

  def _stringitize_reservation(self, dt):
    return '%s  ' % dt.strftime('%I:%M')

  def _pad_len(self, s, length):
    color = self._get_color(s)
    if len(s) > length:
      s = s[:length]
    else:
      s = s + ''.join([' ' for i in range(length - len(s))])
    return s if color == None else colored(s, color)

  def _get_color(self, s):
    return None if not s in COLORED_PHRASES else COLORED_PHRASES[s]
