import argparse

from opentable_restaurant_metadata import write_additional_data
from restaurants_list import get_restaurants

parser = argparse.ArgumentParser(
  description='Get details for a partially data-filled list of restaurants'
  )
parser.add_argument(
  '-input',
  dest='input_file_name',
  required=True,
  help='Path to a file containing a newline-separated list of restaurants with ~ separated data fields',
  )
parser.add_argument(
  '-output',
  dest='output_file_name',
  required=True,
  help='Path to write results to',
  )
args = parser.parse_args()

datas = get_restaurants(args.input_file_name)
for restaurant in datas:
  written = write_additional_data(args.output_file_name, restaurant)
  if not written:
    print 'WARNING: Could not find:', restaurant.name, '(%d)' % restaurant.rid
