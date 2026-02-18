import time
from main_logic import password_generator
from parallel import parallel_passwords

def benchmark(n=50000):
    # sequential
    start = time.time()
    gen = password_generator()
    for _ in range(n):
        next(gen)
    sequential = time.time() - start

    # parallel
    start = time.time()
    parallel_passwords(n)
    parallel = time.time() - start

    return {
        "Последовательно": sequential,
        "Параллельно": parallel
    }
