import csv
import numpy as np
import time

file = open("test.csv", "w", newline=None)

file_writer = csv.writer(file)

file_writer.writerow(["Time", "Data"])

for i in range(10):
    entry = np.random.random()
    now = time.time()
    file_writer.writerow([now, entry])

file.close()
