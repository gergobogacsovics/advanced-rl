import os
from random import sample
from shutil import copy

class_names = ["left", "straight", "right"]

for c in class_names:
  os.makedirs(f"data_balanced/{c}")

class_to_file_count = {}

for c in class_names:
  class_to_file_count[c] = len(os.listdir(f"data/{c}"))
  print(f"'{c}' class has {class_to_file_count[c]} images in total.")
  
min_class_name = min(class_to_file_count, key=class_to_file_count.get)
min_count = class_to_file_count[min_class_name]

print(f"The class with the minimum number of images is '{min_class_name}' with {min_count} images in total.")

for c in class_names:
  print(f"Sampling random images from class {c}")
  
  file_names = os.listdir(f"data/{c}")
  
  files_sampled = sample(file_names, min_count)
  
  for fname in files_sampled:
    copy(src=f"data/{c}/{fname}", dst=f"data_balanced/{c}/{fname}")
  

