import numpy as np

def frac_allocation(total_num: int, proportion: np.ndarray) -> np.ndarray:
    f = proportion / np.sum(proportion)
    res = np.round(total_num * f)
    res[-1] += (total_num - np.sum(res))
    return res

def random_allocation(total_num: int, group_num: int) -> np.ndarray:
    """
    generate a list. The length of the list is [group]. The summation of the list is [total_num]
    """
    a = [np.random.randint(0, total_num) for i in range(group_num - 1)]
    a.append(0)
    a.append(total_num)
    a.sort()

    b = [a[i+1]-a[i] for i in range (group_num)]

    return np.array(b)