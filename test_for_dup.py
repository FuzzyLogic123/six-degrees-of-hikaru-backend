# Open the file for reading
file_path = './data/bullet/2/results.csv'  # Replace with the actual file path
with open(file_path, 'r') as file:
    lines = file.readlines()

# Extract the first element from each line
first_elements = [line.split('|')[0] for line in lines]

# Use a set to keep track of encountered elements
encountered = set()
duplicates = set()

# Check for duplicates
for element in first_elements:
    if element in encountered:
        duplicates.add(element)
    else:
        encountered.add(element)

# Print the duplicates, if any
if duplicates:
    print("Duplicates found in the first element:")
    print(len(duplicates))
    # for duplicate in duplicates:
    #     print(duplicate)
else:
    print("No duplicates found.")
