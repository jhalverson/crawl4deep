#!/usr/bin/env python3

import subprocess

with open('precision_emails.txt') as f:
    lines1 = f.readlines()
with open('list_to_floe_pni.txt') as f:
    lines2 = f.readlines()

lines = lines1 + lines2
netids = [line.split('@')[0] for line in lines]

def extract_record(lines, field):
  for line in lines.split('\n'):
    if (field in line):
      return line.split(':')[1].strip()

header = ('netid', 'name', 'dept', 'status', 'title', 'academic')
records = []
for netid in sorted(netids):
  output = subprocess.run("ldapsearch -x uid=" + netid, shell=True, capture_output=True)
  text = output.stdout.decode("utf-8")
  dept = extract_record(text, 'ou:')
  name = extract_record(text, 'displayName:')
  title = extract_record(text, 'title:')
  stat = extract_record(text, 'pustatus:')
  aca = extract_record(text, 'puacademiclevel:')
  records.append((netid, name, dept, stat, title, aca))

import pandas as pd

df = pd.DataFrame(records, columns=header)
df.to_csv('ug_list.csv', index=True)
