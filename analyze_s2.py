#!/usr/bin/env python3
# coding: utf-8
import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#epsilon = float(input("epsilon␣greedy:␣"))
# time_to_analyze = int(input("time_to_analyze: "))


# 分析用データ
Rg_list = []
Rg2_list = []
S2_list = []
lonlat_freq_dict = {}
car_total_number = 0
max_lat = -90.0
min_lat = 90.0
max_lon = -180.0
min_lon = 180.0
DIVISION = 100

# main

# データファイルの読み込み
#infilename = "destination_coordinates_data0.8.txt"
#infilename = "analyze_rg-cars70-div40-epslion0.8.csv"
#infilename = "analyze_rg-cars70-div40-epslion0.0.csv"
#infilename = "analyze_rg-cars70-div40-epslion0.05.csv"
#infilename = "destination_coordinates_data" + str(epsilon) + ".txt"
infilename = "destination_coordinates_data0.1.txt"
infile = open(infilename, "r")

car_data_lat = {}
car_data_lon = {}

for line in infile:
# データファイルから属性値を抽出
	#print(line)
	data_list = line.replace("\n", "").replace("(", "").replace(")", "" ).split(",")
	#print(data_list)
	car_id = int(data_list[0])
	time = int(data_list[1])
	start_lat = float(data_list[2])
	start_lon = float(data_list[3])
	end_lat = float(data_list[4])
	end_lon = float(data_list[5])
	#print(car_id, time, start_lat, start_lon, end_lat, end_lon)
	#sys.exit(0)

	if car_id not in car_data_lat:
		car_data_lat[car_id] = []
		car_data_lon[car_id] = []
	car_data_lat[car_id].append(end_lat)
	car_data_lon[car_id].append(end_lon)

	#車の総数の導出
	if car_id > car_total_number:
		car_total_number = car_id
	# 地図の緯度・経度の最小値・最大値の導出
	if start_lat > max_lat:
		max_lat = start_lat
	if end_lat > max_lat:
		max_lat = end_lat

	if start_lon > max_lon:
		max_lon = start_lon
	if end_lon > max_lon:
		max_lon = end_lon

	if start_lat < min_lat:
		min_lat = start_lat
	if end_lat < min_lat:
		min_lat = end_lat

	if start_lon < min_lon:
		min_lon = start_lon
	if end_lon < min_lon:
		min_lon = end_lon

DELTA_LAT = (max_lat - min_lat ) / 100
DELTA_LON = (max_lon - min_lon ) / 100
#print(car_total_number)

for car_id in range( 0, car_total_number):
	#Rgの計算
	lat_center = np.average(car_data_lat[car_id])
	lon_center = np.average(car_data_lon[car_id])
	Rg = 0.0
	for i in range(len(car_data_lat[car_id])):
		Rg += (car_data_lat[car_id][i] - lat_center)**2 + (car_data_lon[car_id][i] - lon_center)**2
	Rg /= len(car_data_lon[car_id])
	Rg = np.sqrt(Rg)
	#print(Rg)
	Rg_list.append(Rg)

	#R_g^{(2)}の計算
	for i in range(len(car_data_lat[car_id])):
		lonlat_tuple = (int((car_data_lat[car_id][i]-min_lat)/DELTA_LAT), int((car_data_lon[car_id][i]-min_lon)/DELTA_LON))
		if lonlat_tuple not in lonlat_freq_dict:
			lonlat_freq_dict[lonlat_tuple] = 1
		else:
			lonlat_freq_dict[ lonlat_tuple ] += 1
	top_two_list = sorted(lonlat_freq_dict.items(), key=lambda x:x[1])[-2:]

	lat_center2 = ((DELTA_LAT*top_two_list[0][0][0] + min_lat) + (DELTA_LAT*top_two_list[1][0][0] + min_lat)) / 2
	lon_center2 = ((DELTA_LON*top_two_list[0][0][1] + min_lon) + (DELTA_LON*top_two_list[1][0][1] + min_lon)) / 2

	#print(top_two_list)
	Rg2 =  top_two_list[0][1] * ( (DELTA_LAT*top_two_list[0][0][0] + min_lat - lat_center2)**2 + (DELTA_LON*top_two_list[0][0][1] + min_lon - lon_center2)**2  )
	Rg2 += top_two_list[1][1] * ( (DELTA_LAT*top_two_list[1][0][0] + min_lat - lat_center2)**2 + (DELTA_LON*top_two_list[1][0][1] + min_lon - lon_center2)**2  )
	Rg2 = np.sqrt(Rg2 / (top_two_list[0][1] + top_two_list[1][1]))
	#print(Rg2)
	S2 = Rg2 / Rg
	print(S2)
	if S2 <= 2.0:
		Rg2_list.append(Rg2)
		S2_list.append(S2)


plt.hist(Rg_list)
plt.savefig("Rg_histogram.png")
plt.clf()

plt.hist(Rg2_list)
plt.savefig("Rg2_histogram.png")
plt.clf()

plt.hist(S2_list)
plt.savefig("S2_histogram.png")
plt.clf()
