import csv
import time
import np

file = open('test.csv', newline = None)

csvwriter = csv.writer(file, delimiter=',')

csvwriter.writerow(["Time","Data"])

for i in range(10):
    now = time.time()
    value = np.random.random()
    csvwriter.writerow([now,value])
    time.sleep(1)

file.close()
