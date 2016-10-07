#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This script defines the environment for meta-norms game.
The environment is responsible for maintaining the game,
i.e., 
implementing effects of agent's action,
deciding what the agents see, and
providing cost/reward to the agents.
"""

import os, sys
import numpy

sys.path.insert(0, os.path.abspath(".."))
from norms_game.agent import agent

# game parameters
num_agents = 20
num_games_per_generation = 4
num_generations = 100
num_simulations = 5
# parameters for defection
temptation_to_defect = 3
hurt_suffered_by_others = -1
# parameters for punishment
cost_of_being_punished = -9
enforcement_cost_punishment = -2
# parameters for meta-punishment 
cost_of_being_meta_punished = -9
enforcement_cost_meta_punishment = -2
# parameters for mutation
probability_mutation = 0.01

class meta_norms_game(object):

  bDebug = False

  def __init__(self):
    """Initializer"""
    
    # initialize agents
    self.players_list = []

    temp_agent_properties = numpy.random.randint(8,size=(num_agents,3))
    for idx in range(num_agents):
      temp_boldness = temp_agent_properties[idx,0] / 7.0
      temp_vengefullness = temp_agent_properties[idx,1] / 7.0
      temp_meta_vengefullness = temp_agent_properties[idx,2] / 7.0
      self.players_list.append(
        agent(boldness= temp_boldness,
            vengefulness= temp_vengefullness,
            meta_vengefulness= temp_meta_vengefullness))

    if self.bDebug:
      self.game_stage()

  def game_stage(self):
    """
    Method for simulating one game stage (e.g., Fig. 3).
    Each generation may involve multiple such games.
    """
    
    ## local variables
    probability_defection_seen = numpy.random.uniform()
    score = numpy.zeros( num_agents )
    defects = numpy.zeros( num_agents , dtype=bool)
    # sees: first index corresponds to the observer
    sees = numpy.zeros( (num_agents,num_agents), dtype=bool)
    punishes = numpy.zeros( (num_agents,num_agents), dtype=bool)
    # meta-sees: first index corresponds to the observed
    #           second index corresponds to the non-punisher
    meta_sees = numpy.zeros( (num_agents,num_agents,num_agents), 
        dtype=bool)
    meta_punishes = numpy.zeros( (num_agents,num_agents,num_agents), 
        dtype=bool)

    """
    Note: Implementation can be made concise and faster, by using a 
    single triple-for loop.
    """

    # n-person P.D.
    for idx in range(num_agents):
      if self.players_list[idx].defect_decision(probability_defection_seen):
        defects[idx] = True
        for jdx in range(num_agents):
          if jdx == idx:
            score[jdx] = score[idx] + temptation_to_defect
          else:
            score[jdx] = score[idx] + hurt_suffered_by_others

    # for those agent who defected, check who was seen by who
    for idx in range(num_agents):
      if defects[idx]:
        for jdx in range(num_agents):
          if jdx != idx:
            temp = numpy.random.uniform()
            if temp < probability_defection_seen:
              sees[jdx,idx] = True

    # decide if the observers - punish the defectors
    for idx in range(num_agents):
      if defects[idx]:
        for jdx in range(num_agents):
          if sees[jdx, idx]:
            if self.players_list[jdx].punish_decision():
              score[idx] = score[idx] + cost_of_being_punished
              score[jdx] = score[jdx] + enforcement_cost_punishment
              punishes[jdx,idx] = True

    # for those agent who did not punish a defection, 
    # check who was seen by who
    for idx in range(num_agents):
      if defects[idx]:
        for jdx in range(num_agents):
          if (sees[jdx,idx] and (not punishes[jdx, idx])):
            for kdx in range(num_agents):
              if ( (kdx != idx) and (kdx != jdx) ):
                temp = numpy.random.uniform()
                if temp < probability_defection_seen:
                  meta_sees[kdx,jdx,idx] = True

    # decide if the meta observers - do not punish the defectors
    for idx in range(num_agents):
      if defects[idx]:
        for jdx in range(num_agents):
          if (sees[jdx,idx] and (not punishes[jdx, idx])):
            for kdx in range(num_agents):
              if ( (kdx != idx) and (kdx != jdx) and 
                meta_sees[kdx,jdx,idx]):
                if self.players_list[kdx].meta_punish_decision():
                  score[idx] = score[idx] + cost_of_being_meta_punished
                  score[jdx] = score[jdx] + enforcement_cost_meta_punishment
                  meta_punishes[jdx,idx] = True

  def generation(self):
    """
    Method for simulating one generation of the game.
    Each generation may involve multiple game stages.
    Allows each agent to take actions (defection, punishment, meta-punishment).
    Provides reward based on selected actions.
    """
    raise NotImplementedError

  def mutation(self):
    """Method for simulating mutation"""
    raise NotImplementedError

  def evolution(self):
    """
    Method for simulating evolution.
    Updates population according to their performance.
    Also accounts for mutation.
    """
    raise NotImplementedError

  def simulation(self):
    """
    Simulates one run of the entire simulation incorporating
    multiple generations and the associated evolution.
    """
    raise NotImplementedError

def main():
  experiment = meta_norms_game()

if __name__ == '__main__':
  main()