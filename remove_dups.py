# import csv

# # Read the CSV file and store data in a dictionary
# data = {}
# with open('./data/bullet/2/results.bak', 'r') as file:
#     csv_reader = csv.reader(file, delimiter='|')
#     for row in csv_reader:
#         data[row[0]] = row

# # Write the deduplicated data back to the CSV file
# with open('./data/bullet/2/results.csv', 'w', newline='') as file:
#     csv_writer = csv.writer(file, delimiter='|')
#     for row in data.values():
#         csv_writer.writerow(row)

users1 = []
with open('./data/bullet/2/results.csv', 'r') as file:
    for line in file:
        users1.append(line.split('|')[0])

users2 = []
with open('./data/bullet/2/results.bak', 'r') as file2:
    for line2 in file2:
        users2.append(line2.split('|')[0])

print(set(users2) == set(users1))