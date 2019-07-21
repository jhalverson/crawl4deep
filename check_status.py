#!/usr/licensed/anaconda3/2019.3/bin/python

import subprocess

with open('emails.txt') as f:
    lines = f.readlines()

netids = [line.split('@')[0] for line in lines]

def extract_record(lines, field):
  for line in lines.split('\n'):
    if (field in line):
      return line.split(':')[1].strip()

records = []
for netid in sorted(netids):
  output = subprocess.run("ldapsearch -x uid=" + netid, shell=True, capture_output=True)
  text = output.stdout.decode("utf-8")
  dept = extract_record(text, 'ou:')
  name = extract_record(text, 'displayName:')
  title = extract_record(text, 'title:')
  stat = extract_record(text, 'pustatus:')
  aca = extract_record(text, 'puacademiclevel:')

  output = subprocess.run("finger " + netid, shell=True, capture_output=True)
  text = output.stdout.decode("utf-8")
  office = extract_record(text, 'Office:')

  records.append((netid, name, dept, stat, title, aca, office))

import pandas as pd
header = ('netid', 'name', 'dept', 'status', 'title', 'academic', 'office')
df = pd.DataFrame(records, columns=header)
df.sort_values(by=['dept', 'netid']).reset_index(drop=True).to_html('lammps_users.html', index=True)
