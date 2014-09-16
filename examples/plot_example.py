from matplotlib import pyplot as plt
from matplotlib import animation
import urllib.request
import json
import sys

time_points = 50

data_list = []

fig = plt.figure(figsize=(20, 8))
fig.suptitle("PS201 readings", fontsize=12)

current_plot = plt.subplot2grid((1, 2), (0, 0))
plt.gca().axes.get_xaxis().set_visible(False)
plt.yticks([x for x in range(0, 1001, 100)])

voltage_plot = plt.subplot2grid((1, 2), (0, 1))
plt.gca().axes.get_xaxis().set_visible(False)
plt.yticks([x for x in range(0, 21)])

current_plot.set_ylabel("mA")
voltage_plot.set_ylabel("V")

current_plot.grid(True)
voltage_plot.grid(True)

current_plot.set_ylim(0, 1000)
current_plot.set_xlim(0, time_points)
voltage_plot.set_ylim(0, 20)
voltage_plot.set_xlim(0, time_points)

output_current_line, = current_plot.plot([], 'b', label='Output current')
current_limit_line, = current_plot.plot([], 'g', label='Current limit')
current_plot.legend([output_current_line, current_limit_line],
                    [output_current_line.get_label(), current_limit_line.get_label()])

output_voltage_line, = voltage_plot.plot([], 'b-', label='Output voltage')
target_voltage_line, = voltage_plot.plot([], 'g-', label='Target voltage')
voltage_plot.legend([output_voltage_line, target_voltage_line],
                    [output_voltage_line.get_label(), target_voltage_line.get_label()])

lines = [output_current_line, current_limit_line, output_voltage_line, target_voltage_line]


def get_values():
    request = 'http://localhost:8080/all_values'
    response = urllib.request.urlopen(request)
    str_response = response.readall().decode('utf-8')
    return json.loads(str_response)


def init():
    for line in lines:
        line.set_data([], [])
    return lines


def animate(i):
    try:
        data_list.append(get_values())
    except:
        print("Error connecting to PS201 server")
        sys.exit()

    time_values = [x for x in range(len(data_list))]

    global time_points
    if len(data_list) > time_points:
        time_points *= 2
        current_plot.set_xlim(0, time_points)
        voltage_plot.set_xlim(0, time_points)

    output_current_line.set_data(time_values, [value['output_current_mA'] for value in data_list])
    current_limit_line.set_data(time_values, [value['current_limit_mA'] for value in data_list])
    output_voltage_line.set_data(time_values, [value['output_voltage_V'] for value in data_list])
    target_voltage_line.set_data(time_values, [value['target_voltage_V'] for value in data_list])
    return lines

plt.legend()

anim = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    interval=1000, blit=True)

plt.show()
