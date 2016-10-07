#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This script defines an agent for meta-norms game.
"""

import sys
import random

class agent(object):

  def __init__(self, 
    boldness= 0,
    vengefulness= 0):
    """Initializer"""
    self.boldness = boldness
    self.vengefulness = vengefulness

  def defects(self):
    """Decides whether the agent defects or not."""
    raise NotImplementedError

  def punishes(self):
    """
    Decides whether the agent punishes or not.
    Called only if the agent sees a defection.
    """
    raise NotImplementedError

  def meta_punishes(self):
    """
    Decides whether the agent meta-punishes or not.
    Meta-punishment refers to the punishment given for 
    not punishing a defection.
    Called only if the agent sees absence of justified punishment.
    """
    raise NotImplementedError


