import argparse
import datetime

from opentable_reservations_v2 import find_reservation_availability
from reservation_printer import print_reservations
from restaurants_list import get_restaurants_under_price

parser = argparse.ArgumentParser(
  description='Find reservations for tasting menu restaurants under a price'
  )

parser.add_argument(
  '-listfile',
  dest='list_file',
  required=True,
  help='Enter a file name containing the list of restaurants to consider',
  )
parser.add_argument(
  '-min',
  dest='min_price',
  default='0',
  help='Specify a minimum price you want to pay',
  )
parser.add_argument(
  '-max',
  dest='max_price',
  default='999999999',
  help='Specify a maximum price you want to pay',
  )
parser.add_argument(
  '-dates',
  dest='dates',
  help='Enter comma-separated dates in mm/dd/yyyy',
  required=True
  )
parser.add_argument(
  '-hour',
  dest='hour',
  help='Enter the hour to search around as hh. Defaults to 19.',
  default='19',
  )
parser.add_argument(
  '-people',
  dest='people',
  default=2,
  help='Number of people attending reservation',
  )
parser.add_argument(
  '-noblacklist',
  dest='is_no_blacklist',
  type=bool,
  help='Don\'t use the blacklist',
  default=False,
  )

args = parser.parse_args()

if args.is_no_blacklist:
  print 'not considering the blacklist'

price_range = [int(args.min_price), int(args.max_price)]
restaurants = get_restaurants_under_price(args.list_file, price_range, args.is_no_blacklist)
print 'considering', len(restaurants), 'restaurants...'

dts = []
hour = int(args.hour)
want_today = False
for s in args.dates.split(','):
  dt = datetime.datetime.strptime(s.strip(), '%m/%d/%Y')
  dt = dt.replace(hour=hour, minute=0, second=0, microsecond=0)
  dts.append(dt)

# Map: {rid: {date: [times]}}
# i.e: {2508: {'2016-11-10': ['17:15'], '2016-11-14': ['21:30', '21:00', '17:15']}}
all_info = find_reservation_availability(
  dts,
  map(lambda r: r.rid, restaurants),
  int(args.people),
  )
print ''

print_reservations(dts, restaurants, all_info)
