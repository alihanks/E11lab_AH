import adafruit_bme680
import time
import board
import csv
import busio
import serial
from adafruit_pm25.uart import PM25_UART
import sys

run_time = 10
if len(sys.argv) < 3:
  print("Input arguments: run_time (seconds) file_name")
  exit()
else:
  run_time = int(sys.argv[1])
  file_name = sys.argv[2]

file = open(file_name, "w", newline=None)
csvwriter = csv.writer(file)
csvwriter.writerow(["Time", "Temperature", "Humidity", "Pressure", "Altitude", "Gas", 
                    "PM1.0", "PM2.5", "PM10", 
                    "Particles > 0.3um", "Particles > 0.5um"])

i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

bme680.sea_level_pressure = 1013.25

reset_pin = None

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
pm25 = PM25_UART(uart, reset_pin)

start_time = time.time()
now = start_time
while now < start_time + run_time:
    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    print("Temperature: %0.1f C" % bme680.temperature)
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)
    print("")

    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")

    csvwriter.writerow([time.time(), bme680.temperature, bme680.relative_humidity, 
                        bme680.pressure, bme680.altitude, bme680.gas,
                        aqdata["pm10 standard"], 
                        aqdata["pm25 standard"], 
                        aqdata["pm100 standard"],
                        aqdata["particles 03um"], 
                        aqdata["particles 05um"]])
    now = time.time()
    time.sleep(1)
