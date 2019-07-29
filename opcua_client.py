from opcua import Client
import time

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []




url="opc.tcp://localhost:4840"

client=Client(url)

client.connect()
print("Connected....")


def animate(i,xs, ys):
    Temp = client.get_node("ns=2;i=2")
    Temperature = Temp.get_value()

    Press = client.get_node("ns=2;i=3")
    Pressure = Press.get_value()

    Time = client.get_node("ns=2;i=4")
    Time_value = Time.get_value()

    print(Temperature, " ", Pressure, " ", Time_value)


    xs.append(Time_value)
    ys.append(Temperature)

    xs = xs[-25:]
    ys = ys[-25:]

    ax.clear()
    ax.plot(xs, ys)

    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Temperature over Time')
    plt.ylabel('Temperature (deg C)')




# while True:
#     Temp=client.get_node("ns=2;i=2")
#     Temperature=Temp.get_value()
#
#     Press = client.get_node("ns=2;i=3")
#     Pressure = Press.get_value()
#
#     Time = client.get_node("ns=2;i=4")
#     Time_value = Time.get_value()
#
#     print(Temperature," ",Pressure," ",Time_value)


ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys,), interval=2000)
plt.show()
