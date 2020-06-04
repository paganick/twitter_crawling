import csv

with open('edge_list.csv', 'r') as infile, open('edge_list2.csv', 'a') as outfile:
    # output dict needs a list for new column ordering
    fieldnames = ['Source', 'Target']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)
