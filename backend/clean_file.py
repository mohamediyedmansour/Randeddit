#!/usr/bin/env python3

import os

file_path = "./assets/subreddits.txt"
temp_path = "./assets/subreddits_temp.txt"
count = 0

with open(file_path, "r") as infile, open(temp_path, "w") as outfile:
    for line in infile:
        name = line.split()[0]
        outfile.write(name + "\n")
        count += 1

os.replace(temp_path, file_path)

print(f"found {count} subreddits")
