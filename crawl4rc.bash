#!/bin/bash

# specifiy the path to the home directories
path_to_home_directories=/home

# specifify the search pattern
pattern="*lammps*"

for user in $(ls -d $path_to_home_directories/*)
do
    count=$(find $user -iname $pattern 2>/dev/null | wc -l)
    if [ $count -gt 0 ]; then
      echo $user $count | tee -a count.lammps
    fi
done
