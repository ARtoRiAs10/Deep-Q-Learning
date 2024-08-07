# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 01:41:31 2024

@author: gaurav

"""

# Installing the required libraries
#conda install -c conda-forge tensorflow
#conda install -c conda-forge keras

import os
import numpy as np
import random as rn
import environment
import brain
import dqn

# Setting seeds for reproducibility
os.environ['PYHTONHASHSEED'] = '0'
np.random.seed(42)
rn.seed(12345)

#SETTING THE PARAMETERS
epsilon = .3
number_actions = 5
direction_boundary= (number_actions - 1) /2
number_epochs = 100
max_memory = 3000
batch_size = 512
temperature_Step = 1.5

# BUILDING THE ENVIRONMENT BY SIMPLY CREATING AN OBJECT OF THE ENVIRONMENT CLASS
env = environment.Environment(optimal_temperature = (18.0, 24.0), initial_month= 0, initial_number_users = 20 , initial_rate_data = 30)

# BUILDING THE BRAIN BY SIMPLY CREATING AN OBJECT OF THE BRAIN CLASS
brain = brain.Brain(learning_rate=0.00001, number_actions = number_actions)

# BUILDING THE DQN MODEL BY SIMPLY CREATING AN OBJECT OF THE DQN CLASS
dqn = dqn.DQN( max_memory = max_memory, discount = 0.9)

#CHOOSING THE MODE
train = True


# TRAINING THE AI
env.train = train
model = brain.model
if (env.train) :
    
    for epoch in range(1, number_epochs):
        total_reward = 0
        loss = 0.
        new_month = np.random.randint(0,12)
        env.reset(new_month = new_month)
        game_over = False
        current_state, _ , _ = env.observe()
        timestep = 0
        
        while ((not game_over) and timestep <= 5 *30 * 24 * 60):
            # PLAYING THE NEXT ACTION EXPLORATION
            if np.random.rand() <= epsilon:
                action = np.random.randint(0, number_actions)
                if (action - direction_boundary < 0):
                    direction = -1
                    
                else:
                    direction = 1
                energy_ai = abs(action - direction_boundary) * temperature_Step
                
            # PLAYING THE NEXT ACTION INFERENCE
            else :
                q_values = model.predict(current_state)
                action  = np.argmax(q_values[0])
                if (action - direction_boundary < 0):
                    direction = -1
                    
                else:
                    direction = 1
                energy_ai = abs(action - direction_boundary) * temperature_Step
                
            
            # UPDATING THE ENVIRONMENT AND REACHING THE NEXT STATE
            next_state, reward, game_over = env.update_env( direction, energy_ai, int(timestep / (30 * 24 * 60)))
            total_reward += reward
            
            # STORING THIS NEW TRANSITION INTO THE MEMORY
            dqn.remember([current_state, action, reward, next_state], game_over)
            
            
            # GATHERING IN TWO SEPERATE BATCHES THE INPUTS AAND THE TARGETS
            inputs, targets = dqn.get_batch( model, batch_size = batch_size)
            
            # COMPUTING THE LOSS OVER THE TWO WHOLE BATCHES OF INPUTS AND TARGETS
            loss += model.train_on_batch(inputs, targets)
            timestep += 1
            current_state = next_state
            
            
        # PRINTING THE TRAINING RESULTS FOR EACH EPOCH
        print("\n")
        print("Epoch: {:03d}/{:03d} ".format(epoch, number_epochs))
        print ("Total Energy spent with an AI : {:.0f}".format(env.total_energy_ai ))
        print ("Total Energy spent with no AI : {:.0f}".format(env.total_energy_noai ))
        
        #SAVING THE MODEL
        model.save("model.h5")            
