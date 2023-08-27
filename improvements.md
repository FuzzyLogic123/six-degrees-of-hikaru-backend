Store cheaters in amazon dynamo db (should be free)

That way we don't have to check fair play status for repeat offenders across different archives (hopefully this percentage is big to get a big speed up)

10ms read/write plus network. See if its worthwile to store in dynamo db

Can batch transactions (eg. store entire list of players until the end and then check database for all those keys else make chess.com api request)