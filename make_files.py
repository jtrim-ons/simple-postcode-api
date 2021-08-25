import json
import csv
import re
from pathlib import Path
from collections import Counter

postcode_prefix_counter = Counter()

files = set()

with open("postcode_lookup.csv", "r") as f:
    csvreader = csv.reader(f)
    for i, row in enumerate(csvreader):
        if i == 0:
            headings = row
            continue
        postcode = row[0]
        postcode_prefix = postcode[:2]
        postcode_suffix = postcode[2:].replace(' ', '_')
        postcode_filename = postcode_suffix[:-2]
        postcode_prefix_counter[postcode_prefix] += 1
        Path("intermediate/{}".format(postcode_prefix)).mkdir(parents=True, exist_ok=True)
        filename = 'intermediate/{}/{}.ndjson'.format(postcode_prefix, postcode_filename)
        files.add((postcode_prefix, postcode_filename))
        with open(filename, 'a') as outfile:
            outfile.write('{}\n'.format(json.dumps(row)))
        if i % 10000 == 0:
            print(i)

for postcode_prefix, postcode_filename in files:
    file = 'intermediate/{}/{}.ndjson'.format(postcode_prefix, postcode_filename)
    value_dicts = [{} for _ in headings[1:]]
    compressed_data = {}
    with open(file, "r") as f:
        for row_ in f:
            row = json.loads(row_)
            compressed_row = []
            for item, vals in zip(row[1:], value_dicts):
                if item not in vals:
                    vals[item] = len(vals)
                compressed_row.append(vals[item])
            compressed_data[row[0]] = compressed_row
    value_lists = []
    for vals in value_dicts:
        value_lists.append([key for key, val in sorted(vals.items(), key=lambda keyval: keyval[1])])
    Path("api/{}".format(postcode_prefix)).mkdir(parents=True, exist_ok=True)
    outfile = 'api/{}/{}.json'.format(postcode_prefix, postcode_filename)
    with open(outfile, 'w') as f:
        json.dump({"headings": headings[1:], "values": value_lists, "data": compressed_data}, f, separators=(',', ':'))
