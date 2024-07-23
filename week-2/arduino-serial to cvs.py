import serial
import csv
import datetime

port = 'COM9'
baud_rate = 9600
ser = serial.Serial(port, baud_rate)

csv_file = open('data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['date', 'x', 'y', 'z' ])

try:
    while True:
        date = datetime.datetime.now()
        formatDate = str(date.year) + str(date.month) + str(date.day) + str(date.hour) + str(date.minute) + str(date.second)

        serial_data = ser.readline().decode().strip()
        
        x, y, z = serial_data.split(',')
        csv_writer.writerow([formatDate, x, y, z])
        csv_file.flush()
        
except KeyboardInterrupt:
    pass

csv_file.close()
ser.close()
