#!/usr/bin/env python3

# imports
import rospy
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from apes_anticipation_exp.srv import compute_anticipation, compute_anticipationResponse

# Callback function
def ape_observation_callback(ape_observation):

    # Setting the evidence from ape observation
    evidence = {'Belief': ape_observation.belief, 'TrueState':  ape_observation.loc}
    
    # infering the marginal probabilities from the bayesian model from the evidence using Variable Elimination
    marginal_probabilities = inference.query(variables=['Action'], evidence=evidence)

    return compute_anticipationResponse(marginal_probabilities.values[0])

def bayesian_net():
    # Create a Bayesian network
    model = BayesianNetwork()

    # Define nodes

    # Belief of the human agent
    belief_state = 'Belief'
    # Action of ape agent
    agent_action = 'Action'
    # True state of the object hidden
    true_state = 'TrueState'

    # Add nodes to the model
    model.add_nodes_from([belief_state, agent_action, true_state])

    # Define edges (dependencies)
    model.add_edge(belief_state, agent_action)
    model.add_edge(true_state, agent_action)

    # Define conditional probability distributions (CPTs)
    cpd_belief = TabularCPD(variable=belief_state, variable_card=2, values=[[0.5], [0.5]])
    cpd_true = TabularCPD(variable=true_state, variable_card=2, values=[[0.5], [0.5]])
    cpd_action = TabularCPD(variable=agent_action, variable_card=2, 
                            values=[[1./3, 2./3, 2./3, 1./3], 
                                    [2./3, 1./3, 1./3, 2./3]],
                            evidence=[belief_state, true_state], 
                            evidence_card=[2, 2])

    # Add CPTs to the model
    model.add_cpds(cpd_belief, cpd_true, cpd_action)

    return model


if __name__ == '__main__':

    # Initializing node
    rospy.init_node('bayesian_node Service', anonymous=True)

    # Bayesian model oject
    bayesian_network = bayesian_net()
    # Setting inference to Variable Elimination
    inference = VariableElimination(bayesian_network)

    # number of times apes anticipate the false belief
    anticipation_count = 0

    service = rospy.Service("compute_anticipation", compute_anticipation, ape_observation_callback)

    rospy.spin()
