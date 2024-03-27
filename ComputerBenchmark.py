import numpy as np
import time
import threading

# Define the function to integrate
def f(x):
    return x ** 2

# Define the limits of integration
a = 0
b = 1

# Define the number of intervals for Simpson's rule
n_intervals = 100

# Define the matrix dimensions
rows = 1000
cols = 1000

# Initialize the matrix
matrix = np.zeros((rows, cols))

# Function to perform numerical integration using Simpson's rule
def integrate_simpson(f, a, b, n):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    integral = h / 3 * np.sum(y[0:-1:2] + 4 * y[1::2] + y[2::2])
    return integral

def fill_matrix(start_row, end_row):
    for i in range(start_row, end_row):
        for j in range(cols):
            # Adjust the limits of integration based on the row and column indices
            a_ij = i
            b_ij = i + j + 1
            matrix[i, j] = integrate_simpson(f, a_ij, b_ij, n_intervals)

# Define the number of threads
num_threads = 8

# Divide rows evenly among threads
rows_per_thread = rows // num_threads

times = []

# Fill in the matrix using numerical integration
for k in range(1, 5):
    threads = []
    st = time.time()
    for i in range(0, rows, rows_per_thread):
        t = threading.Thread(target=fill_matrix, args=(i, min(i + rows_per_thread, rows)))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    et = time.time()
    print(k)
    times.append(et - st)

print(matrix)

total_time = 0
for time in times:
    total_time = total_time + time

average_time = total_time / len(times)

print('Execution Time: ', average_time, ' Seconds')
