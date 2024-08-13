import serial
import json
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


databaseURL = 'https://sit225-51p-19166-default-rtdb.firebaseio.com/'
cred_obj = firebase_admin.credentials.Certificate(
    'serviceAccountKey.json'
)
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL':databaseURL
})

ref = db.reference("/")

port = 'COM9'
baud_rate = 9600
ser = serial.Serial(port, baud_rate)

jsonFile = open("data.json", "w")
jsonData = []

try:
    while True:
        date = datetime.datetime.now()
        formatDate = str(date.year) + str(date.month) + str(date.day) + str(date.hour) + str(date.minute) + str(date.second)

        serial_data = ser.readline().decode().strip()
        x, y, z = serial_data.split(', ')

        jsonEntry = {
            "timestamp" : formatDate,
            "x": x,
            "y": y,
            "z": z
        }

        jsonData.append(jsonEntry)

except KeyboardInterrupt:
    pass

json.dump(jsonData, jsonFile, indent=4)
jsonFile.close()

ref.set(jsonData)

ser.close()
