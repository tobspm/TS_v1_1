#!usr/bin/env python
# -*- coding: utf-8 -*-
#Modified date: 18/05/2016
#Nima 
#

import numpy as np
import scipy as sp

import PyKEP as pk

import config
import motion
import gravitational
import trajectory_parser

if __name__ == '__main__':
    host_traj = trajectory_parser.TrajParser()
  
    with open(config.input_dir + config.host_trajectory_file) as input_file:
        t, p, v = host_traj.parse_traj(input_file)

    earth = gravitational.KnownBody("earth")
    acc = earth.sph_acc(t, p)
    print acc

    input_file = "da"
    didymos_a = gravitational.UnKnownBody('didymos_a', 35.351, input_file)
    u_t = 2458500.0
    r, v = didymos_a.eph(u_t)
    print "r: ", r
    print "v: ", v


