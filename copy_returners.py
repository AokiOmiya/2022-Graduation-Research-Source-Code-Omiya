#!/usr/bin/env python3
# coding: utf-8
#
# usage: $ python3 copy_returners.py 
#
import os

with open('returners.txt', 'r') as infile:
  for line in infile:
    cmd = 'cp '
    #print(line)
    cmd += line.replace('\n', '')
    cmd += " cabspottingdata-returners_only/"
    #print(cmd)
    os.system(cmd)

  
