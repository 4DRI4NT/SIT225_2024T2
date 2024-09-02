import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
import datetime
import pandas as pd
import seaborn as sns

DEVICE_ID = "bdda2196-1343-4b28-8206-275d538294cd"
SECRET_KEY = "wRiTRVEIXjE9jb@XbDPy29k2w"

# Default global list
all_list = []


# Continuously saves and graphs data
def continuous_graph(value, axis):
    global all_list

    # Get timestamp
    date = datetime.datetime.now()
    formatDate = str(date.hour) + str(date.minute) + str(date.second)

    # Show values
    print(f"{formatDate}, {value}, {axis}")

    # Add to list
    all_list.append([formatDate, value, axis])

    # Construct dataframe to graph
    df = pd.DataFrame(all_list, columns=['date','value','axis'])
    fig = sns.lineplot(data=df, x='date', y='value', hue='axis').get_figure()

    # Save as image
    fig.savefig('figure_' + formatDate + '.png')

    # Confirm graph update
    print("New graph created")

def on_x_value_changed(client, value):
    continuous_graph(value, 'x')

def on_y_value_changed(client, value):
    continuous_graph(value, 'y')

def on_z_value_changed(client, value):
    continuous_graph(value, 'z')


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