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
import copy, numpy
import pylab as plt

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
probability_mutation = 0.00

class meta_norms_game(object):

  bDebug = False

  def __init__(self):
    """Initializer"""
    
    # initialize agents
    self.players_list = []
    self.score = numpy.zeros( num_agents )

    self.start_population()

    if self.bDebug:
      self.game_stage()
      self.generation()
      print self.flip_bit(0/7.0,2)
      self.mutation()
      self.replication()
      self.evolution()

  #__________________________________________________
  # Helper functions
  def urn_check(self, probability_threshold):
    """Checks go, no-go based on draw from Uniform Random"""
    temp = numpy.random.uniform()
    return (temp<probability_threshold)

  def flip_bit(self, x_float, ith_bit):
    """Flips ith-bit of the variable x_float."""
    x_int = int(round(x_float*7))
    x_temp = list(bin(x_int))[2:]

    if len(x_temp) == 1:
      x_bin = ['0','0',x_temp[0]]
    elif len(x_temp) == 2:
      x_bin = ['0',x_temp[1],x_temp[0]]
    elif len(x_temp) == 3:
      x_bin = x_temp
    else:
      raise RuntimeError

    reverse_ith_bit = -(ith_bit+1)
    if x_bin[reverse_ith_bit] == '0':
      x_bin[reverse_ith_bit] = '1'
    elif x_bin[reverse_ith_bit] == '1':
      x_bin[reverse_ith_bit] = '0'
    else:
      raise RuntimeError

    x_new_int = int(''.join(x_bin),2)
    x_new_float = x_new_int/7.0

    return ( x_new_float )

  #__________________________________________________
  # Simulation functions
  def start_population(self):
    self.players_list = []
    self.score = numpy.zeros( num_agents )
    temp_agent_properties = numpy.random.randint(8,size=(num_agents,3))
    for idx in range(num_agents):
      temp_boldness = temp_agent_properties[idx,0] / 7.0
      temp_vengefulness = temp_agent_properties[idx,1] / 7.0
      temp_meta_vengefulness = temp_agent_properties[idx,2] / 7.0
      self.players_list.append(
        agent(boldness= temp_boldness,
            vengefulness= temp_vengefulness,
            meta_vengefulness= temp_meta_vengefulness))

  def game_stage(self):
    """
    Method for simulating one game stage (e.g., Fig. 3).
    Each generation may involve multiple such games.
    """
    
    ## local variables
    probability_defection_seen = numpy.random.uniform()
    stage_score = copy.deepcopy(self.score)
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
            stage_score[jdx] = stage_score[jdx] + temptation_to_defect
          else:
            stage_score[jdx] = stage_score[jdx] + hurt_suffered_by_others

    # for those agent who defected, check who was seen by who
    for idx in range(num_agents):
      if defects[idx]:
        for jdx in range(num_agents):
          if jdx != idx:
            if self.urn_check(probability_defection_seen):
              sees[jdx,idx] = True

    # decide if the observers - punish the defectors
    for idx in range(num_agents):
      if defects[idx]:
        for jdx in range(num_agents):
          if sees[jdx, idx]:
            if self.players_list[jdx].punish_decision():
              stage_score[idx] = stage_score[idx] + cost_of_being_punished
              stage_score[jdx] = stage_score[jdx] + enforcement_cost_punishment
              punishes[jdx,idx] = True

    # for those agent who did not punish a defection, 
    # check who was seen by who
    for idx in range(num_agents):
      if defects[idx]:
        for jdx in range(num_agents):
          if (sees[jdx,idx] and (not punishes[jdx, idx])):
            for kdx in range(num_agents):
              if ( (kdx != idx) and (kdx != jdx) ):
                if self.urn_check(probability_defection_seen):
                  meta_sees[kdx,jdx,idx] = True

    # decide if the meta observers - do not punish the defectors
    for idx in range(num_agents):
      if defects[idx]:
        for jdx in range(num_agents):
          if ((not punishes[jdx, idx])):
            for kdx in range(num_agents):
              if ( (kdx != idx) and (kdx != jdx) and 
                meta_sees[kdx,jdx,idx]):
                if self.players_list[kdx].meta_punish_decision():
                  stage_score[jdx] = ( stage_score[jdx] + 
                    cost_of_being_meta_punished )
                  stage_score[kdx] = ( stage_score[kdx] + 
                    enforcement_cost_meta_punishment )
                  meta_punishes[jdx,idx] = True

    # save score
    self.score = copy.deepcopy(stage_score)

  def generation(self):
    """
    Method for simulating one generation of the game.
    Each generation may involve multiple game stages.
    Allows each agent to take actions (defection, punishment, meta-punishment).
    Provides reward based on selected actions.
    """
    for _ in range(num_games_per_generation):
      self.game_stage()

  def mutation_deprecated(self):
    """Method for simulating mutation"""
    for idx in range(num_agents):
      for id_bit in range(3):
        # mutate boldness
        if self.urn_check(probability_mutation):
          self.players_list[idx].boldness = self.flip_bit(
            self.players_list[idx].boldness, id_bit )
        # mutate vengefulness
        if self.urn_check(probability_mutation):
          self.players_list[idx].vengefulness = self.flip_bit(
            self.players_list[idx].vengefulness, id_bit )
        # mutate meta_vengefulness
        if self.urn_check(probability_mutation):
          self.players_list[idx].meta_vengefulness = self.flip_bit(
            self.players_list[idx].meta_vengefulness, id_bit )

  def mutation(self):
    """Method for simulating mutation"""
    for idx in range(num_agents):
      if self.urn_check(probability_mutation):
        for id_bit in range(3):
          # mutate boldness
          self.players_list[idx].boldness = self.flip_bit(
            self.players_list[idx].boldness, id_bit )
          # mutate vengefulness
          self.players_list[idx].vengefulness = self.flip_bit(
            self.players_list[idx].vengefulness, id_bit )
          # mutate meta_vengefulness
          self.players_list[idx].meta_vengefulness = self.flip_bit(
            self.players_list[idx].meta_vengefulness, id_bit )

  def replication(self):
    """
    Method for simulating replication.
    Updates population according to their performance.
    Also accounts for mutation.
    """
    # replicate based on score
    mean_score = self.score.mean()
    std_score = self.score.std()
    new_players_list = []
    for idx in range(num_agents):
      if self.score[idx] < (mean_score - std_score):
        # one standard deviation below is not replicated
        pass
      elif self.score[idx] > (mean_score + std_score):
        # one standard deviation above is replicated twice
        new_players_list.append(self.players_list[idx])
        new_players_list.append(self.players_list[idx])
      else:
        # average score (within one standard deviation)
        new_players_list.append(self.players_list[idx])

    # ensure population size remains fixed
    while (len(new_players_list) != num_agents):
      len_temp = len(new_players_list)
      random_idx = numpy.random.randint(len_temp)
      if (len_temp < num_agents):
        # add one player
        new_players_list.append(new_players_list[random_idx])
      else:
        # remove one player
        del new_players_list[random_idx]

    # reset player list and score
    del self.players_list[:]
    self.players_list = new_players_list
    self.score = numpy.zeros( num_agents )

    # perform mutation
    self.mutation()

  def evolution(self):
    """
    Simulates one run of the entire evolution incorporating
    multiple generations and the associated replication.
    """

    # perform generation and replication computations
    self.start_population()
    for _ in range(num_generations):
      self.generation()
      self.replication()

    # compute end of evolution parameters
    boldness_array = numpy.empty(0)
    vengefulness_array = numpy.empty(0)
    meta_vengefulness_array = numpy.empty(0)
    for player in self.players_list:
      boldness_array = numpy.append(boldness_array, player.boldness)
      vengefulness_array = numpy.append(vengefulness_array, 
        player.vengefulness)
      meta_vengefulness_array = numpy.append(meta_vengefulness_array, 
        player.meta_vengefulness)

    print "    Boldness    ,  Vengefulness  , Metavengfulness " 
    print "    %.4f      ,     %.4f     ,     %.4f     " % (
      boldness_array.mean(),
      vengefulness_array.mean(),
      meta_vengefulness_array.mean())
    print "    %.4f      ,     %.4f     ,     %.4f     " % (
      boldness_array.std(),
      vengefulness_array.std(),
      meta_vengefulness_array.std())

    return (boldness_array.mean(),
      vengefulness_array.mean(),
      meta_vengefulness_array.mean(),
      boldness_array.std(),
      vengefulness_array.std(),
      meta_vengefulness_array.std())

  def simulation(self):
    """Simulates multiple indpendent time-histories of evolution."""
    simulation_summary = []
    for _ in range(num_simulations):
      evolution_summary = self.evolution()
      simulation_summary.append(evolution_summary)
    return simulation_summary

def plot_summary(summary_list):
  """Plots the summary values from the experiment"""
  tempX = []
  tempY = []
  tempZ = []
  for idx in range(num_simulations):
    tempX.append( summary_list[idx][0] )
    tempY.append( summary_list[idx][1] )
    tempZ.append( summary_list[idx][2] )

  temp_font = {'size': 22}
  plt.rc('font',**temp_font)
  plt.plot(tempX,tempY,'ks',markersize=20)
  plt.xlabel('Boldness')
  plt.ylabel('Vengefulness')
  temp_title = ( 'P = ' + str(cost_of_being_punished) + '\n'
    r"""P' = """  + str(cost_of_being_meta_punished) )
  plt.title(temp_title, fontsize=20)
  plt.grid()
  plt.xlim(0,1)
  plt.ylim(0,1)
  fig_title = '../graphs/P' + str(cost_of_being_punished) + \
    r"""P'"""  + str(cost_of_being_meta_punished) + '.svg'
  plt.savefig(fig_title, bbox_inches='tight')

def main():
  experiment = meta_norms_game()
  experiment_summary = experiment.simulation()
  plot_summary(experiment_summary)

if __name__ == '__main__':
  main()