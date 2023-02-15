import gym
from util import simplify_observation
import matplotlib.pyplot as plt
import cv2
import keyboard
import os

NUM_EPISODES = 10
SEED = 42

print("Creating directory structure...")
os.makedirs("data/left")
os.makedirs("data/straight")
os.makedirs("data/right")

env = gym.make("CarRacing-v2", domain_randomize=False, render_mode="human")

env.action_space.seed(SEED)

img_indices = {
    "left": 0,
    "straight": 0,
    "right": 0
}

observation, info = env.reset(seed=SEED)
done = False
frames_to_skip = 120
frame_idx = 0

while not done:
    if frame_idx < frames_to_skip:
        env.step([0, 0, 0])
        frame_idx += 1
        continue
    
    steering = 0

    if keyboard.is_pressed("a"):
        steering = -1  
    elif keyboard.is_pressed("d"):
        steering = +1
    elif keyboard.is_pressed("esc"):
        terminate = True
        break

    action = [steering, 0.01, 0]
    observation, reward, done, truncated, info = env.step(action)

    obs = simplify_observation(observation)

    if steering == -1:
        directory = "left"
    elif steering == +1:
        directory = "right"
    else:
        directory = "straight"

    img_idx = img_indices[directory]

    cv2.imwrite(f"data/{directory}/{img_idx}.jpg", cv2.cvtColor(obs, cv2.COLOR_RGB2BGR))

    img_indices[directory] += 1

    if done:
        observation, info = env.reset()

cv2.destroyAllWindows()
env.close()
