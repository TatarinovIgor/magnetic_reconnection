import numpy as np
import sys
from scipy.signal import find_peaks


dataset = np.loadtxt("datasets/solar_cycle_23",
                     dtype=float)

np.set_printoptions(suppress=True)
np.set_printoptions(threshold=sys.maxsize)

distance_between_locals = 1000
date_range_hour = 72

dates = []

date_year = dataset[:,0]
date_day = dataset[:,1]
date_hour = dataset[:,2]

plasma_temp = dataset[:, 4]
proton_density = dataset[:, 5]
plasma_speed = dataset[:, 6]


my_len = len(plasma_speed) - 1
i = 0
print(my_len)
while (i < my_len):
    print(i)
    if plasma_temp[i] > 9999990:
        plasma_temp = np.delete(plasma_temp, i, 0)
        proton_density = np.delete(proton_density, i, 0)
        plasma_speed = np.delete(plasma_speed, i, 0)
        my_len = my_len - 1

        continue

    if proton_density[i] > 990:
        plasma_temp = np.delete(plasma_temp, i, 0)
        proton_density = np.delete(proton_density, i, 0)
        plasma_speed = np.delete(plasma_speed, i, 0)
        my_len = my_len - 1


        continue

    if plasma_speed[i] > 9990:
        plasma_temp = np.delete(plasma_temp, i, 0)
        proton_density = np.delete(proton_density, i, 0)
        plasma_speed = np.delete(plasma_speed, i, 0)
        my_len = my_len - 1


        continue
    i = i + 1

plasma_temp_peaks, _ = find_peaks(plasma_temp, distance=distance_between_locals)
proton_density_peaks, _ = find_peaks(proton_density, distance=distance_between_locals)
plasma_speed_peaks, _ = find_peaks(plasma_speed, distance=distance_between_locals)

#print(plasma_temp_peaks)
#print(proton_density_peaks)
#print(plasma_speed_peaks)

final_j = 0
final_i = 0
final_k = 0

subset1 = []

# idk how this works tbh
for i in range(len(plasma_temp_peaks)):
    subset1.append([plasma_temp_peaks[i]])

    for j in range(len(proton_density_peaks)):
        if (abs(subset1[i][0] - proton_density_peaks[j]) < date_range_hour):
            subset1[i].append(proton_density_peaks[j])


len_temp_peaks = len(plasma_temp_peaks)
i = 0
while i < len_temp_peaks:
    if len(subset1[i]) <= 1:
        subset1.pop(i)
        len_temp_peaks = len_temp_peaks - 1
    else:
        i = i + 1

for j in range(len(subset1)):
    subset1[j].append(date_range_hour - abs(subset1[j][0] - subset1[j][1]))

subset2 = []
for i in range(len(subset1)):
    for j in range(len(plasma_speed_peaks)):
        if (abs(subset1[i][0] - plasma_speed_peaks[j]) < subset1[i][2]):
            subset2.append([subset1[i][0], subset1[i][1], plasma_speed_peaks[j]])
            dates.append([date_year[j], date_day[j], date_hour[j]])
        if (abs(subset1[i][1] - plasma_speed_peaks[j]) < subset1[i][2]):
            subset2.append([subset1[i][0], subset1[i][1], plasma_speed_peaks[j]])
            dates.append([date_year[j], date_day[j], date_hour[j]])

my_len = len(subset2) - 1
i = 0
while (i < my_len):
    if ((subset2[i][0] == subset2[i + 1][0]) and (subset2[i][1] == subset2[i + 1][1]) and (
            subset2[i][2] == subset2[i + 1][2])):
        dates.pop(i + 1)
        subset2.pop(i + 1)
        my_len = my_len - 1

    i = i + 1
print("data:")
print(subset2)
print("dates:")
print(dates)
#print()
#print()
#print("PlASMA TEMP:")
#print(plasma_temp)
#print("PROTON DENSITY:")
#print(proton_density)
#print("PLASMA SPEED")
#print(plasma_speed)