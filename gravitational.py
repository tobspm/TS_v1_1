#!usr/bin/env python
# -*- coding: utf-8 -*-
#Modified date: 20/05/2016
#Nima 
#

import numpy as np
import scipy as sp

import PyKEP as pk

import config
import model_tensor

class KnownBody(model_tensor.BaseModel):
    """Class defining the gravitational model of bodies known from PyKEP.

     Attributes defined here:
    -name: the name of the body
    -mu: the gravitational parameter of the body

    Method defined here:
    -sph_acc(): gives the main potential acceleration of body.
    """
    def __init__(self, name):
	"""Constructor of the class KnownBody."""
	model_tensor.BaseModel.__init__(self, name)
	self.body = pk.planet.jpl_lp("%s" % name)
	self.mu = self.body.mu_self
    def __repr__(self):
	"""Method displaying a customized message when an instance of the 
	class KnownBody is called in the command line.
	"""
	return "KnownBody: name = '{}', mu = {} m³/s²".format(self.name,
	self.body.mu_self)
    def relative_position(self, date, satellite_position):
	"""Gives the relative position of the spacecraft with respect to 
	known body. Returns a vector position.
	self.body.eph(date) is a method from PyKEP library providing the 
	ephemeris of self.body: it returns a tuple (r, v) respectively 
	the self.body position and velocity vectors.
	"""
	body_position, _ = np.array(self.body.eph(date))
	r_p = satellite_position - body_position
	return r_p

class UnKnownBody(model_tensor.BaseModel):
    """Class defining the gravitational model of bodies unknown from PyKEP.

    Attributes defined here:
    -name: the name of the unknown body
    -mu: the gravitational parameter of the unknown body
    -traj_file: name of trajectory file of the unknown body ephemeris.

    Method defined here:
    -eph(): gives the ephemeris of unknown body with respect to an epoch
    -sph_acc():
    """
    def __init__(self, name, mu, traj_file):
	"""Constructor of the class UnKnownBody."""
	model_tensor.BaseModel.__init__(self, name)
	self.mu = mu
	self.traj_file = traj_file
    def __repr__(self):
	"""Method displaying a customized message when an instance of the 
	class UnKnownBody is called in the command line.
	"""
	return "UnKnownBody: name = '{}', mu = {} m³/s²".format(self.name,
	self.mu)
    def eph(self, date):
	"""Method providing the ephemeris of unknown body at a given epoch.
	Returns a tuple r, v.
	"""
	with open(config.bodies_input_dir + getattr(config, "%s" % self.traj_file)) as input_file:
	    for line in input_file.read().splitlines(True):
	        values = [float(element) for element in line.split(' ')]
	        time = values[0]
		r = np.array([values[1], values[2], values[3]])
	        v = np.array([values[4], values[5], values[6]])
		
		if (time == date):
		    return r, v
		#r = r * ((time1 - date) / (time1 - time)) + r1 * ((date - time) / (time1 - time))
		#v = v * ((time1 - date) / (time1 - time)) + v1 * ((date - time) / (time1 - time))
	    return r, v
	   






