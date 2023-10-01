import numpy as np


def calculate_moments(array: list | np.ndarray,
                      k: int,
                      central: bool = False):
    if type(array) == 'list':
        array = np.array(list)
    if central:
        array = array - np.mean(array)
    return np.sum(array ** k) / len(array)


normal = np.random.normal(loc=5,
                          scale=4,
                          size=1000000)

calculate_moments(normal, 1)
