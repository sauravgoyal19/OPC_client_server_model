# Simulated OPC UA server: exposes a "Parameters" object with Temperature,
# Pressure and Time variables that update on a timer, standing in for a real
# industrial sensor/PLC endpoint so the client/publisher scripts have
# something to connect to end-to-end.
from opcua import ua, Server
from random import randint
import datetime
import time

server = Server()

url = r"opc.tcp://localhost:4840"
server.set_endpoint(url)

name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)

# Every OPC UA server exposes its data as nodes under the standard "Objects"
# node; we add one custom object ("Parameters") with three child variables.
node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

Temp = Param.add_variable(addspace, "Temperature", 0)
Press = Param.add_variable(addspace, "Pressure", 0)
Time = Param.add_variable(addspace, "Time", 0)

Temp.set_writable()
Press.set_writable()
Time.set_writable()

server.start()

print("Server started at {}".format(url))

# Push a new random reading every 2 seconds, simulating live sensor data.
while True:
    Temperature = randint(10, 50)
    Pressure = randint(100, 900)
    TIME = datetime.datetime.now()
    print(Temperature, Pressure, TIME)
    Temp.set_value(Temperature)
    Press.set_value(Pressure)
    Time.set_value(TIME)

    time.sleep(2)