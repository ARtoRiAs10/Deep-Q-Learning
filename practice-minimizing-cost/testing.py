# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 01:41:32 2024

@author: gaurav
"""
# Installing the required libraries
#conda install -c conda-forge tensorflow
#conda install -c conda-forge keras

import os
import numpy as np
import random as rn
import environment
from keras.models import load_model

# Setting seeds for reproducibility
os.environ['PYHTONHASHSEED'] = '0'
np.random.seed(42)
rn.seed(12345)

#SETTING THE PARAMETERS
number_actions = 5
direction_boundary= (number_actions - 1) /2
temperature_Step = 1.5

# BUILDING THE ENVIRONMENT BY SIMPLY CREATING AN OBJECT OF THE ENVIRONMENT CLASS
env = environment.Environment(optimal_temperature = (18.0, 24.0), initial_month= 0, initial_number_users = 20 , initial_rate_data = 30)

# LOADING A PRE TRAINED BRAIN
model = load_model("model.h5")

#CHOOSING THE MODE
train = False


# RUNNING A 1 YEAR SIMULATION IN INFERENCE MODE
env.train = train
current_state, _ , _ = env.observe()
for timestep in range(0, 12 * 30 * 24 * 60):
    q_values = model.predict(current_state)
    action  = np.argmax(q_values[0])
    if (action - direction_boundary < 0):
        direction = -1
        
    else:
        direction = 1
    energy_ai = abs(action - direction_boundary) * temperature_Step
    next_state, reward, game_over = env.update_env( direction, energy_ai, int(timestep / (30 * 24 * 60)))
    current_state = next_state
            
    
# PRINTING THE TRAINING RESULTS FOR EACH EPOCH
print("\n")
print ("Total Energy spent with an AI : {:.0f}".format(env.total_energy_ai ))
print ("Total Energy spent with no AI : {:.0f}".format(env.total_energy_noai ))
print ("Energy saved: {:.0f } %".format((env.total_energy_noai - env.total_energy_ai) / env.total_energy_noai) * 100)

          
