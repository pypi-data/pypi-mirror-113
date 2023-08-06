from .cocunirandom import Random

_random = Random()

seed = _random.seed
random = _random.random
randint = _random.randint
choice = _random.choice
shuffle = _random.shuffle
