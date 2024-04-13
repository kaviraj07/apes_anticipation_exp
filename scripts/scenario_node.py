#!/usr/bin/env python3

# imports
import rospy
import random
from apes_anticipation_exp.msg import scenario_var

# function for simulating the scenario
def simulate_scenario():

    states = scenario_var()
    # Simulate the scenario events
    # Generate random location of object
    obj_loc = random.choice([0,1])

    # Update belief of human agent
    belief = obj_loc

    states.belief = belief

    # Randomly change location of object
    obj_loc = random.choice([0,1])
    states.loc = obj_loc

    # Publish the scenario variables
    scenario_state.publish(states)

    # logging to know the stage reached
    rospy.loginfo("Scenario States Published")



if __name__ == '__main__':
    # initializing node
    rospy.init_node('scenario_node', anonymous=True)
    
    # initializing object location publisher
    scenario_state = rospy.Publisher('scenario_variables', scenario_var, queue_size=10)

    rate = rospy.Rate(2)# Publish at 10 Hz

    while not rospy.is_shutdown():
        simulate_scenario()
        rate.sleep()