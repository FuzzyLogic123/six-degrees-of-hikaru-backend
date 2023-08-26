INPUT_FILE = "./data/bullet/3/results.csv"
OUTPUT_FILE = "./data/bullet/3/results_bots_removed.csv"

with open('./data/bots.txt', 'r') as filter_strings_file:
    bots = set(filter_strings_file.read().splitlines())

with open(INPUT_FILE, 'r') as input_file, open(OUTPUT_FILE, 'a') as output_file:
    for line in input_file:
        username = line.split('|')[0]
        
        if username not in bots:
            output_file.write(line)

