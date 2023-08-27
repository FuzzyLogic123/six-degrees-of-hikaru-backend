users1 = set()
with open('./data/blitz/3/url_fetch_failures.txt', 'r') as file:
    for line in file:
        users1.add(line)

with open ('./data/blitz/3/failures_no_dup.txt', 'w') as file:
    for user in users1:
        file.write(user)
