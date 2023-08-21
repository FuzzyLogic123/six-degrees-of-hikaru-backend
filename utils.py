# the degree that you are currently trying to calculate
def get_usernames_found_set(time_control, degree):
    degree = degree - 1
    paths_found_usernames = set()

    file_paths = [f'./data/{time_control}/{i}/results.csv' for i in range(int(degree))]
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            next(file) # skip header
            for line in file:
                username = line.strip().split('|')[0]
                paths_found_usernames.add(username)
    print(len(paths_found_usernames))
    return paths_found_usernames


# degree that you are currently trying to calculate
def get_root_players(degree, time_control):
    degree = degree - 1
    root_players = set()

    file_path = f'./data/{time_control}/{degree}/results.csv'
    with open(file_path, 'r') as file:
        next(file) # skip header
        for line in file:
            username = line.strip().split('|')[0]
            root_players.add(username)
    return root_players