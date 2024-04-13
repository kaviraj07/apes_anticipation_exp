#!/usr/bin/env python3

# imports
import rospy
from apes_anticipation_exp.msg import anticipation_count
import matplotlib.pyplot as plt

# Callback function
def plotter(data):
    
    # Clearing the plot
    plt.clf()
    plt.bar(['Correct Belief Anticipation', 'Wrong Belief Anticipation'], [data.ant_count, 30 - data.ant_count], color=['red', 'green'])
    plt.ylabel('Count')
    plt.title('Count of Belief Anticipations')
    plt.pause(0.01)
    plt.draw()

if __name__ == '__main__':

    # Initializing node
    rospy.init_node('plotter', anonymous=True)
    # Setting up subscriber to get aggregated count of 30 experiment
    rospy.Subscriber('ape_anticipation_count', anticipation_count, plotter)
    plt.ion()
    plt.show()
    rospy.spin()