import argparse

from opentable_restaurant_metadata import write_restaurant

parser = argparse.ArgumentParser(
  description='Get details for a list of restaurants'
  )
parser.add_argument(
  '-list',
  dest='list_file_name',
  required=True,
  help='Path to a file containing a newline-separated list of restaurants',
  )
parser.add_argument(
  '-output',
  dest='output_file_name',
  required=True,
  help='Path to write results to',
  )
args = parser.parse_args()


def print_line(line):
  print '  - ' + str(line)

f = open(args.list_file_name, 'r')
lines = f.read().strip().split('\n')
f.close()

sad = []
for line in lines:
  written = write_restaurant(args.output_file_name, line)
  if not written:
    sad.append(line)

print 'Could not find details for:'
map(lambda i: print_line(i), sad)
