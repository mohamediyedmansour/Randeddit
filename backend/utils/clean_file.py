#!/usr/bin/env python3
import os

file_path = "./assets/subreddits.txt"
temp_path = "./assets/subreddits_temp.txt"

kept_count = 0
removed_count = 0
removed_examples = []

with open(file_path, "r") as infile, open(temp_path, "w") as outfile:
    for line in infile:
        name = line.split()[0].strip()
        
        if name.startswith("u_"):
            removed_count += 1
            if len(removed_examples) < 10: 
                removed_examples.append(name)
            continue

        outfile.write(name + "\n")
        kept_count += 1

os.replace(temp_path, file_path)

print(f"Kept {kept_count} subreddits")
print(f"Removed {removed_count} subreddits")
if removed_examples:
    print("Some removed entries:", ", ".join(removed_examples))
