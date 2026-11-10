
import os
import time

def karatsuba(x, y):

    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))

    m = n // 2

    power = 10 ** m

    a = x // power
    b = x % power

    c = y // power
    d = y % power

    z0 = karatsuba(b, d)
    z2 = karatsuba(a, c)
    z1 = karatsuba(a + b, c + d)

    result = (z2 * (10 ** (2 * m))
              + (z1 - z2 - z0) * power
              + z0)

    return result

def read_file(filename):

    with open(filename, 'r') as file:

        x = int(file.readline().strip())
        y = int(file.readline().strip())

    return x, y

def main():

    folder = "Integer_Multiplication"

    os.makedirs("Results", exist_ok=True)

    result_file = open(
        "Results/multiplication_results.txt", "w"
    )

    for filename in sorted(os.listdir(folder)):

        if filename.endswith(".txt"):

            filepath = os.path.join(folder, filename)

            x, y = read_file(filepath)

            digits = max(len(str(x)), len(str(y)))

            start = time.perf_counter()

            result = karatsuba(x, y)

            end = time.perf_counter()

            execution_time = end - start

            if result != x * y:
                print("Error: Incorrect multiplication!")
                continue

            output = f"""
Dataset: {filename}
Number of Digits: {digits}
Multiplication Result: {result}
Execution Time: {execution_time:.6f} seconds
"""

            print(output)
            result_file.write(output)

    result_file.close()

    print("All multiplication datasets processed successfully")

if __name__ == "__main__":
    main()