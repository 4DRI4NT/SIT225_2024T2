import serial
import csv
import datetime

port = 'COM9'
baud_rate = 9600
ser = serial.Serial(port, baud_rate)

csv_file = open('data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["temperature", "humidity"])

try:
    while True:
        serial_data = ser.readline().decode().strip()
        
        temp, hum = serial_data.split(',')
        csv_writer.writerow([hum, temp])
        csv_file.flush()
        
except KeyboardInterrupt:
    pass

csv_file.close()
ser.close()