#!/bin/bash

# Jonathan Halverson (halverson@princeton.edu)
# July 2019

# This Bash script crawls home directories looking for file and
# directory names that match a pattern. It outputs to file the
# count for users with at least one match. It is essentially
# running this command for each home directory, for example:
#   find . -iname '*lammps*' | wc -l

# The script requires two positional arguments. The first is
# the path to the home directories and the second is the
# search term (e.g., matlab).

# Example usage:
#     bash crawl4rc.bash /home lammps
#     bash crawl4rc.bash /home gromacs
#     bash crawl4rc.bash /volume2/Users lammps

if [ $# -lt 2 ]; then
    echo "Please specify a path and search term. Exiting ..."
    exit
fi

# list of home directories
home_directories=$(find $1 -maxdepth 1 -mindepth 1 -type d | sort)

# search pattern
pattern="$2"

outfile="count.$pattern"
echo `hostname` > $outfile
echo `date` >> $outfile
echo "$*" >> $outfile

echo -e "Crawling ...\n"
for user in $home_directories; do
    count=$(find $user -iname "*$pattern*" 2>/dev/null | wc -l)
    if [ $count -gt 0 ]; then
      echo $user $count | tee -a $outfile
    fi
done

echo -e "\nDone. Output written to $outfile."
