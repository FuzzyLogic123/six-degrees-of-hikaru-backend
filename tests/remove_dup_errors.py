users1 = set()
with open('./data/bullet/3/failures.txt', 'r') as file:
    for line in file:
        users1.add(line)

with open ('./data/bullet/3/failures_no_dup.txt', 'w') as file:
    for user in users1:
        file.write(user)
