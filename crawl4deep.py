##################################################################
# Jonathan Halverson (halverson@princeton.edu)
# Monday, June 17, 2019

# This Python 3 script crawls directories looking for filenames
# that match a list of patterns. It outputs the count for each 
# pattern for each user.

# Save this script in your home directory then cd to the directory
# containing the user directories and run it (e.g.,):

# cd $HOME
# wget https://raw.githubusercontent.com/jhalverson/crawl4deep/master/crawl4deep.py
# cd /home
# python3 $HOME/crawl4deep.py > $HOME/output.out

# It produces 2 files: output.out and count.dat
##################################################################

import os
import time

root = os.getcwd()
files = os.listdir(root)
files = list(map(lambda x: os.path.join(root, x), files))
dirs = list(filter(lambda u: os.path.isdir(u), files))
readable_dirs = list(filter(lambda u: os.access(u, os.R_OK), dirs))
readable_dirs.sort()
print('total: %d, directories: %d, readable directores: %d'
      % (len(files), len(dirs), len(readable_dirs)))
print('\n')

inDIRs = ['/.conda', '/.local', '/programs', '/software', '/sw', '/apps']
inDIRs = ['/']
patterns = ['*torch*', '*tensorflow*', '*keras*', '*theano*', '*caffe*',
            '*deeplearning4j*', '*cntk*', '*mxnet*', '*fastai*']

other = []
for pattern in patterns:
  other.append('site-packages/' + pattern.replace('*',''))
  other.append('pkgs/' + pattern.replace('*',''))

print("Appending to count.dat ...\n")

import fnmatch
import grp
import subprocess
from functools import reduce

counts = []
myusers = []
for user in readable_dirs:
  fileList = []
  for inDIR in inDIRs:
    for dName, sdName, fList in os.walk(user + inDIR):
      for fileName in fList:
        for pattern in patterns:
          absFile = os.path.join(dName, fileName)
          if (fnmatch.fnmatch(fileName.lower(), pattern)) and \
             ('site-packages/sympy' not in absFile) and \
             ('site-packages/distributed' not in absFile):
            fileList.append(absFile)
  if (fileList != []):
    newest = max(os.path.getatime(user), os.path.getmtime(user), os.path.getctime(user))
    mytime = int((time.time() - newest) / (3600 * 24))
    group_name = grp.getgrgid(os.stat(user).st_gid)[0]
    mycounts = [user.split('/')[-1], group_name, mytime]
    myusers.append(user)
    group_name = grp.getgrgid(os.stat(user).st_gid)[0]
    if (len(fileList) < 25):
      print(fileList)
      print(user, group_name)
      print(subprocess.check_output("ls -ld " + user, shell=True))
    else:
      stp = len(fileList) // 25
      print(fileList[::stp])
      print(user, group_name)
      print(subprocess.check_output("ls -ld " + user, shell=True))
    print("Total files: ", len(fileList))
    for pattern in patterns:
      cnt = sum([fnmatch.fnmatch(fileName, pattern) for fileName in fileList])
      mycounts.append(cnt)
      if cnt: print('%4d %s' % (cnt, pattern))
    for pattern in other:
      cnt = sum([pattern in fileName for fileName in fileList])
      mycounts.append(cnt)
      if cnt: print('%4d %s' % (cnt, pattern))
    counts.append(mycounts)
    with open(os.environ['HOME'] + '/count.dat', 'a') as f:
      f.write(reduce(lambda u,v: u + ' ' + v, map(str, mycounts)) + '\n')
    print('\n')
print(counts)
