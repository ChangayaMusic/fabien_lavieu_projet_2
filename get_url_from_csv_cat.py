import csv
csv_import_links = []
with open('categories.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    print(row)
    csv_import_links = row
