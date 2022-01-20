#!/usr/bin/env python3
# coding: utf-8
#
# usage: $ python3 taxicab_rg.py cabspottingdata/new*txt
#
import sys
import matplotlib.pyplot as plt
import numpy as np

savefig_dir = "./cabspottingdata-figs/"
Rg_list = []
Rg2_list = []
S2_list = []
lonlat_freq_dict = {}
LATITUDE_MIN = 37.57917
LATITUDE_MAX = 37.84091
LONGITUDE_MIN = -122.54083
LONGITUDE_MAX = -122.35087
DIVISION = 100
DELTA_LAT = (LATITUDE_MAX-LATITUDE_MIN)/100
DELTA_LON = (LONGITUDE_MAX-LONGITUDE_MIN)/100


# main
infilename_list = sys.argv[1:]
#print(infilename_list, len(infilename_list))

for infilename in infilename_list:
  longitude_list = []
  latitude_list = []
  infile = open(infilename, 'r')
  for line in infile:
    #print(line)
    data_list = line.replace("\n", "").split(" ")
    #print(data_list)
    latitude = float(data_list[0])
    longitude = float(data_list[1])
    if latitude >= LATITUDE_MIN and longitude >= LONGITUDE_MIN and latitude < LATITUDE_MAX and longitude < LONGITUDE_MAX:
      latitude_list.append(latitude)
      longitude_list.append(longitude)
  infile.close()
  #print(latitude_list)
  #print(longitude_list)
#  plt.plot(longitude_list, latitude_list, linestyle="", marker=".")
#  plt.savefig(savefig_dir+infilename.split("/")[-1].replace(".txt", "")+".png")
#  plt.clf()

  # calculation of R_g
  lat_center = np.average(latitude_list)
  lon_center = np.average(longitude_list)
  Rg = 0.0
  for i in range(len(longitude_list)):
    Rg += (latitude_list[i] - lat_center)**2 + (longitude_list[i] - lon_center)**2
  Rg /= len(longitude_list)
  Rg = np.sqrt(Rg)
  #print(Rg)
  Rg_list.append(Rg)

  # calculate R_g^{(2)}
  for i in range(len(longitude_list)):
    lonlat_tuple = (int((latitude_list[i]-LATITUDE_MIN)/DELTA_LAT), int((longitude_list[i]-LONGITUDE_MIN)/DELTA_LON))
    if lonlat_tuple not in lonlat_freq_dict:
      lonlat_freq_dict[ lonlat_tuple ] = 1
    else:
      lonlat_freq_dict[ lonlat_tuple ] += 1
  top_two_list = sorted(lonlat_freq_dict.items(), key=lambda x:x[1])[-2:]

  lat_center2 = ((DELTA_LAT*top_two_list[0][0][0] + LATITUDE_MIN) + (DELTA_LAT*top_two_list[1][0][0] + LATITUDE_MIN)) / 2
  lon_center2 = ((DELTA_LON*top_two_list[0][0][1] + LONGITUDE_MIN) + (DELTA_LON*top_two_list[1][0][1] + LONGITUDE_MIN)) / 2

  #print(top_two_list)
  Rg2 =  top_two_list[0][1] * ( (DELTA_LAT*top_two_list[0][0][0] + LATITUDE_MIN - lat_center2)**2 + (DELTA_LON*top_two_list[0][0][1] + LONGITUDE_MIN - lon_center2)**2  ) 
  Rg2 += top_two_list[1][1] * ( (DELTA_LAT*top_two_list[1][0][0] + LATITUDE_MIN - lat_center2)**2 + (DELTA_LON*top_two_list[1][0][1] + LONGITUDE_MIN - lon_center2)**2  )
  Rg2 = np.sqrt(Rg2 / (top_two_list[0][1] + top_two_list[1][1]))
  #print(Rg2)
  S2 = Rg2 / Rg
  print(S2)
  if S2 <= 2.0:
    Rg2_list.append(Rg2)
    S2_list.append(S2)
#  elif S2 <= 2.0:
#    Rg2_list.append(Rg2)
#    S2_list.append(1.0)
  #break

plt.hist(Rg_list)
plt.savefig("Rg_histogram.png")
plt.clf()

plt.hist(Rg2_list)
plt.savefig("Rg2_histogram.png")
plt.clf()

plt.hist(S2_list)
plt.savefig("S2_histogram.png")
plt.clf()

