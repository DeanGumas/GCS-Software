import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import csv
import sys
import serial
from xbee import XBee

class Index(object):

    def send_command(self, event):
        print("Command Sent!\n")

fig, ((ax_alt, ax_press, ax_temp), (ax_volt, ax_lat, ax_lon), (ax_gps_alt, ax_gps_sats, ax_pitch), (ax_roll, ax_spin, ax_state)) = plt.subplots(4,3)

fig.set_size_inches(18.5, 12.5)

line, = ax_alt.plot(np.random.rand(10))
line2, = ax_press.plot(np.random.rand(10))
line3, = ax_temp.plot(np.random.rand(10))
line4, = ax_volt.plot(np.random.rand(10))
line5, = ax_lat.plot(np.random.rand(10))
line6, = ax_lon.plot(np.random.rand(10))
line7, = ax_gps_alt.plot(np.random.rand(10))
line8, = ax_gps_sats.plot(np.random.rand(10))
line9, = ax_pitch.plot(np.random.rand(10))
line10, = ax_roll.plot(np.random.rand(10))
line11, = ax_spin.plot(np.random.rand(10))
line12, = ax_state.plot(np.random.rand(10))


# set Altitude Graph
ax_alt.set_ylim(0, 1000)
ax_alt.set(title='Altitude (m)')

# set pressure Graph
ax_press.set_ylim(0, 150000)
ax_press.set(title='Pressure (Pa)')

# Set Temperature Graph
ax_temp.set_ylim(0,100)
ax_temp.set(title='Temperature (C)')

# Set Voltage Graph
ax_volt.set_ylim(0,5)
ax_volt.set(title='Voltage (V)')

# Set Latitude Graph
ax_lat.set_ylim(35, 39)
ax_lat.set(title='Latitude (Deg)')

# Set Longitude Graph
ax_lon.set_ylim(75, 85)
ax_lon.set(title='Longitude (Deg)')

# Set GPS Altitude Graph
ax_gps_alt.set_ylim(0, 1000)
ax_gps_alt.set(title='GPS Altitude (m)')

# Set GPS sats Graph
ax_gps_sats.set_ylim(0, 30)
ax_gps_sats.set(title='Satellites in View')

# Set pitch Graph
ax_pitch.set_ylim(0, 360)
ax_pitch.set(title='Pitch (Deg)')

# Set Roll Graph
ax_roll.set_ylim(0, 360)
ax_roll.set(title='Roll (Deg)')

# Set Spin Rate Graph
ax_spin.set_ylim(0, 1000)
ax_spin.set(title='Spin (rpm)')

# Set State Graph
ax_state.set_ylim(0, 10)
ax_state.set(title='Software State')

xdata, gps_sats_data, pitch_data, roll_data, spin_data, state_data, alt_data, press_data, temp_data, volt_data, lat_data, lon_data, gps_alt_data = [0]*100, [0]*100, [0]*100, [0]*100, [0]*100, [0]*100, [0]*100, [0]*100, [0]*100, [0]*100, [0]*100, [0]*100, [0]*100

callback = Index()
ax_button = plt.axes([0.7, 0.02, 0.075, 0.05])

b_command = Button(ax_button, 'Calibrate')
b_command.on_clicked(callback.send_command)


f = open('Flight_1.csv', 'a')

try:
    ser = serial.Serial("COM5", 9600)
except:
    ser = serial.Serial()

xbee = XBee(ser)



def update(data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12):
    line.set_ydata(data)
    line2.set_ydata(data1)
    line3.set_ydata(data2)
    line4.set_ydata(data3)
    line5.set_ydata(data4)
    line6.set_ydata(data5)
    line7.set_ydata(data6)
    line8.set_ydata(data7)
    line9.set_ydata(data8)
    line10.set_ydata(data9)
    line11.set_ydata(data10)
    line12.set_ydata(data11)
    return line, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12

def run(data):
    t, alt, press, temp, volt, lat, lon, gps_alt, gps_sats, pitch, roll, spin, state = data
    del xdata[0]
    del alt_data[0]
    del press_data[0]
    del temp_data[0]
    del volt_data[0]
    del lat_data[0]
    del lon_data[0]
    del gps_alt_data[0]
    del gps_sats_data[0]
    del pitch_data[0]
    del roll_data[0]
    del spin_data[0]
    del state_data[0]

    xdata.append(t)
    alt_data.append(alt)
    press_data.append(press)
    temp_data.append(temp)
    volt_data.append(volt)
    lat_data.append(lat)
    lon_data.append(lon)
    gps_alt_data.append(gps_alt)
    gps_sats_data.append(gps_sats)
    pitch_data.append(pitch)
    roll_data.append(roll)
    spin_data.append(spin)
    state_data.append(state)

    #ax[0].plot(xdata, ydata, xdata, y1data)
    line.set_data(xdata, alt_data)
    line2.set_data(xdata, press_data)
    line3.set_data(xdata, temp_data)
    line4.set_data(xdata, volt_data)
    line5.set_data(xdata, lat_data)
    line6.set_data(xdata, lon_data)
    line7.set_data(xdata, gps_alt_data)
    line8.set_data(xdata, gps_sats_data)
    line9.set_data(xdata, pitch_data)
    line10.set_data(xdata, roll_data)
    line11.set_data(xdata, spin_data)
    line12.set_data(xdata, state_data)
    return line, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12

def data_gen():
    t = 0
    while True:
        t+=0.1
        try:
            alt = 0
            press = 0
            temp = 0
            volt = 0
            lat = 0
            lon = 0
            gps_alt = 0
            gps_sats = 0
            pitch = 0
            roll = 0
            spin = 0
            state = 0
            count = 0

            #temp = ser.readline()
            #data_line = str(temp.decode())
            #f.write(data_line + "\n")

            print("waiting")
            temp = xbee.wait_read_frame()
            print(temp)
            data_line = str(temp.decode())
            f.write(data_line + "\n")

            for x in data_line.split(','):
                if count == 1:
                    press = float(x)
                elif count == 4:
                    press = float(x)
                elif count == 5:
                    temp = float(x)
                elif count == 6:
                    volt = float(x)
                elif count == 8:
                    lat = float(x)
                elif count == 9:
                    lon = float(x)
                elif count == 10:
                    gps_alt = float(x)
                elif count == 11:
                    gps_sats = int(x)
                elif count == 12:
                    pitch = int(x)
                elif count == 13:
                    roll = int(x)
                elif count == 14:
                    spin = int(x)
                elif count == 15:
                    state = int(x)
                elif count > 15:
                    break

                count = count + 1

        except:
            alt = 0
            press = 0
            temp = 0
            volt = 0
            lat = 0
            lon = 0
            gps_alt = 0
            gps_sats = 0
            pitch = 0
            roll = 0
            spin = 0
            state = 0
        yield t, alt, press, temp, volt, lat, lon, gps_alt, gps_sats, pitch, roll, spin, state

if __name__== '__main__':
    ani = animation.FuncAnimation(fig, run, data_gen, interval=100, blit=True)
    plt.show()
