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
sys.path.insert(0, os.path.abspath(".."))

from norms_game.agent import agent

# game parameters
num_agents = 20
num_games_per_generation = 4
num_generations = 100
num_simulations = 5
# parameters for defection
probability_defection_seen = 0.5
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

  def __init__(self):
    """Initializer"""
    
    # initialize agents
    raise NotImplementedError

  def sim_game_stage(self):
    """
    Method for simulating one game stage (e.g., Fig. 3).
    Each generation may involve multiple such games.
    """
    raise NotImplementedError

  def sim_generation(self):
    """
    Method for simulating one generation of the game.
    Allows each agent to take actions (defection, punishment, meta-punishment).
    Provides reward based on selected actions.
    """
    raise NotImplementedError

  def sim_mutation(self):
    """Method for simulating mutation"""
    raise NotImplementedError

  def sim_evolution(self):
    """
    Method for simulating evolution.
    Updates population according to their performance.
    Also accounts for mutation.
    """
    raise NotImplementedError

  def sim_simulation(self):
    """
    Simulates one run of the entire simulation incorporating
    multiple generations and the associated evolution.
    """
    raise NotImplementedError