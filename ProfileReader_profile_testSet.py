# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 11:49:35 2019

@author: Cristina Ponte Lira
"""

###############################################################################
# How to use Profile.py
#
#
###############################################################################

# Use Profule.py

import Profile as P

###############################################################################
# Ribeira
#tanP 0.03 | xP 0.85 | zB 3.1 | tanB 0.06

#read profile file in .npy format
A = P.Profile('profile_testSet_RI_20091023.npy',platform_slope=0.03,
              y_rocky_coastline=0.85)

# plot the profile
A.plot() 

#calculate volume of sandybeach
A.sandy_volArea(platform_slope=0.03,y_rocky_coastline=0.85, lower_bound = -2,
                right_bound = 90, upper_bound=5)

#plot calculated volume 
A.plot_volumeArea()
