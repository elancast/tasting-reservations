import argparse
import datetime

from opentable_reservations import get_reservations_for_list
from reservation_printer import print_reservations
from restaurants_list import get_restaurants_under_price

parser = argparse.ArgumentParser(
  description='Find reservations for tasting menu restaurants under a price'
  )

parser.add_argument(
  '-price',
  dest='price',
  help='Specify a max price you want to pay',
  )
parser.add_argument(
  '-dates',
  dest='dates',
  help='Enter comma-separated dates in mm/dd/yyyy',
  required=True
  )
parser.add_argument(
  '-people',
  dest='people',
  default=2,
  help='Number of people attending reservation',
  )

args = parser.parse_args()

restaurants = get_restaurants_under_price(args.price)
print 'considering', len(restaurants), 'restaurants...'

dates = []
want_today = False
for s in args.dates.split(','):
  date = datetime.datetime.strptime(s.strip(), '%m/%d/%Y').date()
  dates.append(date)
  want_today = want_today or date == datetime.date.today()

# Date we pass in doesn't matter - it can even be in the past! - just want time
now = datetime.datetime.now()
tonight = now.replace(hour=19, minute=0, second=0, microsecond=0)

all_info = get_reservations_for_list(
  tonight,
  map(lambda r: r.rid, restaurants),
  int(args.people),
  want_today,
  )
print ''
print ''

print_reservations(dates, restaurants, all_info)
