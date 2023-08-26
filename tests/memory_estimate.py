import sys
import random

object_size = sys.getsizeof({
    "player_losses": set([str(random.random()) for _ in range(100)])
})

set_size = sys.getsizeof(set([str(random.random()) for _ in range(1000)]))

total_memory = (object_size + set_size) * 18000

total_memory = total_memory / 1024**3

print(f"Approximate memory usage: {total_memory} gigabytes")