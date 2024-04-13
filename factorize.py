import multiprocessing
import time

def factorize_single(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_parallel(numbers):
    num_processes = multiprocessing.cpu_count()
    start_time = time.time()
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(factorize_single, numbers)
    end_time = time.time()
    execution_time = end_time - start_time
    return results, execution_time

if __name__ == '__main__':
    numbers = (128, 255, 99999, 10651060)
    results, execution_time = factorize_parallel(numbers)

    print("Factors:")
    for i, number in enumerate(numbers):
        print(f"Factors of {number}: {results[i]}")
    print(f"Execution time: {execution_time} seconds")
