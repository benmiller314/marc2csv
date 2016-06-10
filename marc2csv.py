# Simple marc2csv script.

import csv
import user
import sys

from pymarc import MARCReader

filepath = 'data.mrc'
infield_delim = ' | '

if len(sys.argv) > 1:
    filepath = sys.argv[1]

try:
    reader = MARCReader(open(filepath))
except IOError:
    print >>sys.stderr, 'cannot open "%s"' % filepath
    sys.exit(1)

csv_records = []
marc_tags = []

for marc_record in reader:
    csv_record = {}
    for marc_field in marc_record.fields: 
        if marc_field.tag not in marc_tags:
            marc_tags.append(marc_field.tag)
        if not csv_record.get(marc_field.tag):
            csv_record[marc_field.tag] = marc_field.value()
        else:
            csv_record[marc_field.tag] += infield_delim + str(marc_field.value())
    csv_records.append(csv_record)

marc_tags.sort()

print ','.join(['"%s"' % tag for tag in marc_tags])
writer = csv.DictWriter(sys.stdout, marc_tags)
writer.writerows(csv_records)
