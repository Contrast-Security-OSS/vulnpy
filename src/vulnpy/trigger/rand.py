"""
Using an insecure random number generator doesn't require user input.

To keep things interesting we reseed the random number generator with
the user's input. This is not necessary for the vulnerability to be present.
"""

import random


def _seed(user_input):
    """
    For seeding to be deterministic in PY2 we need to pass in an integer
    """
    random.seed(user_input)


def do_random(user_input):
    _seed(user_input)
    return str(random.random())


def do_randint(user_input):
    _seed(user_input)
    return str(random.randint(0, 100))


def do_randrange(user_input):
    _seed(user_input)
    return str(random.randrange(0, 101, 5))


def do_uniform(user_input):
    _seed(user_input)
    return str(random.uniform(5.5, 7.5))
