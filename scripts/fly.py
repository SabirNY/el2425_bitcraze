#!/usr/bin/env python

import sys
import rospy
from std_srvs.srv import Empty
from el2425_bitcraze.srv import SetGoal

# Enable the takeoff service. This assumes the crazyflie position is accurately estimated by the LPS system. 
# It might take a few seconds for the ekf to converge so wait before running this

if __name__ == "__main__":
    # Wait for services to become available
    rospy.loginfo("waiting for services")
    rospy.wait_for_service('/crazyflie/takeoff')
    rospy.wait_for_service('/crazyflie/land')
    rospy.wait_for_service('/crazyflie/setgoal')
    rospy.loginfo("found services")
    
    # Service call functions
    takeoff = rospy.ServiceProxy('/crazyflie/takeoff', Empty)
    land = rospy.ServiceProxy('/crazyflie/land', Empty)
    setgoal = rospy.ServiceProxy('/crazyflie/setgoal', SetGoal)
    
    # Parse goal from terminal
    try:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
        z = float(sys.argv[3])

        # Set initial goal position and takeoff!
        setgoal(x,y,z)
        takeoff()

        #Wait for user to press any key and then land
        raw_input("Press any key to land")
        land()
    except Exception,e:
        print(e)
        print("\n")
        print('Please specify correct hover coordinates, e.g.: fly.py -1.0 1.0 1.0') 
