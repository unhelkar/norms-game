#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This script defines an agent for meta-norms game.
"""

import sys
import numpy

class agent(object):

  def __init__(self, 
    boldness= 0,
    vengefulness= 0,
    meta_vengefulness= 0):
    """Initializer"""
    self.boldness = boldness
    self.vengefulness = vengefulness
    self.meta_vengefulness = meta_vengefulness

  def defects(self, probability_defection_seen):
    """Decides whether the agent defects or not."""
    defect_decision = (probability_defection_seen < self.boldness)
    return defect_decision

  def punishes(self):
    """
    Decides whether the agent punishes or not.
    Called only if the agent sees a defection.
    """
    temp = numpy.random.uniform()
    punish_decision = (temp < self.vengefulness)
    return punish_decision

  def meta_punishes(self):
    """
    Decides whether the agent meta-punishes or not.
    Meta-punishment refers to the punishment given for 
    not punishing a defection.
    Called only if the agent sees absence of justified punishment.
    """
    temp = numpy.random.uniform()
    meta_punish_decision = (temp < self.meta_vengefulness)
    return meta_punish_decision