import gym
from util import simplify_observation
import matplotlib.pyplot as plt
import cv2
import keyboard
import os
import tensorflow as tf
from tensorflow.keras import datasets, models
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import numpy as np

NUM_EPISODES = 10
SEED = 42
PREDICTION_FREQUENCY = 5

class_names = ["left", "straight", "right"]

batch_size = 32
img_height = 56
img_width = 56

def load_model(path):
    model = models.Sequential([
        Conv2D(32, (3, 3), activation="relu", input_shape=(img_height, img_width, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation="relu"),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation="relu"),
        Flatten(),
        Dense(64, activation="relu"),
        Dense(3)
    ])
    
    model.load_weights(path)
    
    return model

def preprocess_observation(obs):
    return np.expand_dims(obs / 255, axis=0)

env = gym.make("CarRacing-v2", domain_randomize=False, render_mode="human")

env.action_space.seed(SEED)

model = load_model("model/my_model.h5")

terminate = False

for episode in range(NUM_EPISODES):
    if terminate:
        break
    
    observation, info = env.reset(seed=SEED)
    done = False
    frames_to_skip = 120
    frame_idx = 0
    predictions = [0, 1, 0]
    
    while not done:
        if frame_idx < frames_to_skip:
            observation, reward, done, truncated, info = env.step([0, 0, 0])
            obs = simplify_observation(observation)
            
            frame_idx += 1
            
            continue
        if frame_idx % PREDICTION_FREQUENCY == 0:
            predictions = model.predict(preprocess_observation(obs), verbose=0)[0]
            frame_idx = frames_to_skip
        
        action_idx = np.argmax(predictions, axis=0)
        action_name = class_names[action_idx]
        
        steering = 0
        
        if action_name == "left":
            steering = -1  
        elif action_name == "right":
            steering = +1
        #elif action_name == "straight":
        #    steering = 0
        if keyboard.is_pressed("esc"):
            terminate = True
            break

        action = [steering, 0.01, 0]
        observation, reward, done, truncated, info = env.step(action)

        obs = simplify_observation(observation)

        if done:
            observation, info = env.reset()
            
        frame_idx += 1

env.close()
