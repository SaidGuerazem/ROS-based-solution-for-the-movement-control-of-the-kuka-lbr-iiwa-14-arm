from client_lib import *
import time

if __name__ == '__main__':
    my_client = kuka_iiwa_ros_client()  # Making a connection object.
while (not my_client.isready):
        pass  # Wait until iiwa is connected zzz!
print('Started')

# Initializing Tool 1
my_client.send_command('setTool tool1')

# Initializing
my_client.send_command('setJointAcceleration 0.2')
my_client.send_command('setJointVelocity 0.2')
my_client.send_command('setJointJerk 0.2')
my_client.send_command('setCartVelocity 100')
# Move close to a start position.
my_client.send_command('setPosition 0 49.43 0 -48.5 0 82.08 0')
# Move to the exact start position.
my_client.send_command('setPositionXYZABC 700 0 300 -180 0 -180 ptp')  # ptp motions move with setJointAcceleration


# Robot is compliant in XY plain.
print('Robot is compliant in XY plain.')
my_client.send_command('setCompliance 10 10 5000 300 300 300')
time.sleep(30) # Specify the adequate time here
# Compliance OFF
my_client.send_command('resetCompliance') 