#!/usr/bin/python
# coding=utf-8
'''
@file: fly_line.py
@brief: To control the quadrotor to a given position(not far away!) using pid control method.
@author: Peng Cheng
@date: 2015/10/27  cpeng@zju.edu.cn

'''
import time
from droneapi.lib import VehicleMode, Location
from pymavlink import mavutil
import sys, math

# function: record currrent time(s)
current_milli_time = lambda: int(time.time() * 1000)

# First get an instance of the API endpoint
api = local_connect()
# Get the connected vehicle (currently only one vehicle can be returned).
vehicle = api.get_vehicles()[0]

# theta: the angle of polar coordinate
# v_max: the velocity of polar oordinate
theta = -30 * math.pi / 180
v_max = 2

# get the command parameter

'''
print len(sys.argv)
print sys.argv
if len(sys.argv) <= 1:
	print "Please input like this: 'fly_line.py theta'. theta=[-180, 180]!"
elif len(sys.argv) == 2:
	theta = sys.argv[1]
	print theta
'''
# function: takeoff to the target height
def arm_and_takeoff(aTargetAltitude):
	print "Basic pre-arm checks"
	if vehicle.mode.name == "INITIALISING":
		print "Waiting for vehicle to initialise"
		time.sleep(1)
	while vehicle.gps_0.fix_type < 2:
		print "Waiting for GPS........", vehicle.gps_0.fix_type
		time.sleep(1)

	print "Arming motors"

	vehicle.mode = VehicleMode("GUIDED")
	vehicle.armed = True
	vehicle.flush()

	while not vehicle.armed and not api.exit:
		print "Waiting for arming..."
		time.sleep(1)

	print "Take off!"
	vehicle.commands.takeoff(aTargetAltitude)
	vehicle.flush()

	#Wait until the vehicle reaches a safe height
	while not api.exit:
		print "Altitude: ", vehicle.location.alt
		if vehicle.location.alt >= aTargetAltitude*0.95:
			print "Reached target altitude"
			break;
		time.sleep(1)

# function: controlling vehicle movement using velocity
# Set up velocity mappings
# velocity_x > 0 => fly North
# velocity_x < 0 => fly South
# velocity_y > 0 => fly East
# velocity_y < 0 => fly West
# velocity_z < 0 => ascend
# velocity_z > 0 => descend
def send_ned_velocity(velocity_x, velocity_y, velocity_z):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
    # send command to vehicle
    vehicle.send_mavlink(msg)
    vehicle.flush()

# Get Vehicle Home location ((0 index in Vehicle.commands)
print "Get home location" 
cmds = vehicle.commands
cmds.download()
cmds.wait_valid()
print " Home WP: %s" % cmds[0]

send_ned_velocity(0, 1, 0)

delt_T = 1000   #ms
loop_cnt = 1
lastRecord = current_milli_time()

# open or create a file
f = file('/home/odroid/multiDrone_Com/test_modules/fly_datalog','a+')

arm_and_takeoff(3.0)

while not api.exit:
	if current_milli_time() - lastRecord >= delt_T: #1s
		lastRecord = current_milli_time()
		print "[%s] current time is: %f" % (loop_cnt, lastRecord)
		
		loop_cnt += 1

		send_ned_velocity(v_max*math.sin(theta), v_max*math.cos(theta), 0)
		print "vx: %f; vy: %f" % (v_max*math.sin(theta), v_max*math.cos(theta))
		realV = vehicle.velocity  #[vx, vy, vz]
		f.write(str(current_milli_time())+' '+str(realV[0])+' '+str(realV[1])+' ')
		f.write(str(vehicle.location.lat)+' '+str(vehicle.location.lon)+'\n')

vehicle.mode = VehicleMode("LAND")
f.close

