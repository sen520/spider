import csv
filename = './data/安丘.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_cow = next(reader)
    print(header_cow)
    first_row = next(reader)
    print(first_row)
