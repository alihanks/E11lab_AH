import sys
import time

print(sys.argv)

run_time = int(sys.argv[1])
count = 0
while count < run_time:
  count += 1
  print("Taking data entry:",count)
  time.sleep(1)
