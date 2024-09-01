import sys
import traceback
import random
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
import datetime
import csv
from csv import writer
import pandas as pd
import matplotlib as plt
import plotly.express as px
import seaborn as sns

DEVICE_ID = "bdda2196-1343-4b28-8206-275d538294cd"
SECRET_KEY = "wRiTRVEIXjE9jb@XbDPy29k2w"

# Default values
list = []
save_list = []


def add_to_list(value, time, axis):
    global list
    global save_list

    list.append([time, value, axis])

    if len(list) > 20:
        save_list = list
        list_to_graph()
        list.clear()
        save_list.clear()

def list_to_graph():
    global save_list

    df = pd.DataFrame(save_list, columns=['date','value','axis'])
    df = df.sort_values('date').reset_index(drop=True)
    fig = sns.lineplot(data=df, x='date', y='value', hue='axis').get_figure()
    fig.savefig('figure_' + df.loc[1, 'date'] + '.png')
    print("New graph saved")

def on_x_value_changed(client, value):
    date = datetime.datetime.now()
    formatDate = str(date.hour) + str(date.minute) + str(date.second)
    print(f"{formatDate}, {value}")
    add_to_list(value, formatDate, 'x')

def on_y_value_changed(client, value):
    date = datetime.datetime.now()
    formatDate = str(date.hour) + str(date.minute) + str(date.second)
    print(f"{formatDate}, {value}")
    add_to_list(value, formatDate, 'y')

def on_z_value_changed(client, value):
    date = datetime.datetime.now()
    formatDate = str(date.hour) + str(date.minute) + str(date.second)
    print(f"{formatDate}, {value}")
    add_to_list(value, formatDate, 'z')


def main():
    # Instantiate Arduino cloud client
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )

    client.register(
        "x_value", value=None, 
        on_write=on_x_value_changed)

    client.register(
        "y_value", value=None, 
        on_write=on_y_value_changed)

    client.register(
        "z_value", value=None, 
        on_write=on_z_value_changed)

    # start cloud client
    client.start()


if __name__ == "__main__":
    try:
        main()  # main function which runs in an internal infinite loop
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)