from time import time
from pprint import pprint
from multiprocessing import Pool, current_process, cpu_count
import logging
from random import randint

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def factorize(*numbers):
    timer_fun = time()
    results = []
    for num in numbers:
        num_res = _factorize(num)
        results.append(num_res)
        logging.debug(f'pid={current_process().pid}, {num} Operation time: {time()-timer_fun}')
    return results


def _factorize(num):
    divider = [i for i in range(1, num+1) if num % i == 0]
    return divider


if __name__ == '__main__':
    logger.debug(f'Start programm')
    timer = time()

    numbers = []
    for el in range(25):
        numbers.append(randint(10000, 1000000))

    with Pool(processes=cpu_count()) as pool:
        result = pool.map(factorize, iterable=numbers)
        logger.debug(result)

    logger.debug(f'End program, Total time {time() - timer}')