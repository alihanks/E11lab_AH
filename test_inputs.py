import sys
import time

print(sys.argv)

run_time = int(sys.argv[1])

count = 0
while count < run_time:
  print(count)
  count += 1
  time.sleep(1)
