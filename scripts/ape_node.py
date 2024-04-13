#!/usr/bin/env python3

# imports
import rospy
from apes_anticipation_exp.msg import apes_anticipation, anticipation_count, scenario_var
from apes_anticipation_exp.srv import compute_anticipation

def scenario_state_callback(scenario_state):

    # setting a global count
    global anticipation_counter
    global exp_count

    # reading the variables from the scenario
    obj_loc = scenario_state.loc
    belief = scenario_state.belief
    
    exp_count += 1
   
    # Calling service
    rospy.wait_for_service("compute_anticipation")

    try:
        # Getting the anticipation marginal probabilities from service
        ant_res = compute_anticipation_service(belief,obj_loc)
        ant_left = ant_res.loc_ant
        ant_right = 1 - ant_left

        ape_ant = apes_anticipation()

        if ant_left > ant_right:
            ape_ant.loc_ant = 0
            # checking if belief matches anticipation, then increment counter
            if belief == 0:
                anticipation_counter += 1

        elif ant_left < ant_right:
            ape_ant.loc_ant = 1
            # checking if belief matches anticipation, then increment counter
            if belief == 1:
                anticipation_counter += 1
        
        # Publish the anticipation of the ape for rqt_plot
        ape_observation_pub.publish(ape_ant)
        
        # logging to know the stage reached
        rospy.loginfo("Anticipation Published")

        ape_ant_count = anticipation_count()
        # After 30 experiments, publish to aggregated count of correct anticipations
        if exp_count == 30:
            ape_ant_count.ant_count = anticipation_counter
            ape_counter_pub.publish(ape_ant_count)
            anticipation_counter = 0
            exp_count = 0
            rospy.loginfo("30 Experiments complete - Publishing correct anticipations")

    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


if __name__ == '__main__':
    # Node initialization
    rospy.init_node('ape_node', anonymous=True)

    # number of times apes anticipate the correct belief
    anticipation_counter = 0

    # count for the number of experiment
    exp_count = 0

    # Initilizing publishers
    ape_counter_pub = rospy.Publisher('ape_anticipation_count', anticipation_count, queue_size=10)
    ape_observation_pub = rospy.Publisher('ape_anticipation', apes_anticipation, queue_size=10)

    # Setting up bayesian service
    compute_anticipation_service = rospy.ServiceProxy("compute_anticipation",compute_anticipation)

    # Setting up subscriber
    rospy.Subscriber('scenario_variables', scenario_var, scenario_state_callback)

    rospy.spin()