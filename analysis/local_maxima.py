import numpy as np
import sys
from scipy.signal import find_peaks

dataset = np.loadtxt("datasets/test_dataset.txt",
                     dtype=float)

np.set_printoptions(suppress=True)
np.set_printoptions(threshold=sys.maxsize)
distance_between_locals = 10
date_range_hour = 24
dates = []
date_year = dataset[:, 0]
date_day = dataset[:, 1]
date_hour = dataset[:, 2]
plasma_temp = dataset[:, 3]
proton_density = dataset[:, 4]
plasma_speed = dataset[:, 5]
my_len = len(plasma_speed) - 1
i = 0
print(my_len)
while (i < my_len):
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
plasma_temp_peaks_indexes, _ = find_peaks(plasma_temp, distance=distance_between_locals)
proton_density_peaks, _ = find_peaks(proton_density, distance=distance_between_locals)
plasma_speed_peaks, _ = find_peaks(plasma_speed, distance=distance_between_locals)
# print(plasma_temp_peaks)
# print(proton_density_peaks)
# print(plasma_speed_peaks)
final_j = 0
final_i = 0
final_k = 0
subset1 = []
# idk how this works tbh
for i in range(len(plasma_temp_peaks_indexes)):
    subset1.append([plasma_temp_peaks_indexes[i]])

    for j in range(len(proton_density_peaks)):
        if (abs(subset1[i][0] - proton_density_peaks[j]) < date_range_hour):
            subset1[i].append(proton_density_peaks[j])
            break
len_temp_peaks = len(plasma_temp_peaks_indexes)
i = 0
# redundant
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
            subset2.append([subset1[i][0], subset1[i][1], int(plasma_speed_peaks[j])])
        if (abs(subset1[i][1] - plasma_speed_peaks[j]) < subset1[i][2]):
            subset2.append([subset1[i][0], subset1[i][1], int(plasma_speed_peaks[j])])
my_len = len(subset2) - 1
i = 0
while (i < my_len):
    if ((subset2[i][0] == subset2[i + 1][0]) and (subset2[i][1] == subset2[i + 1][1]) and (
            subset2[i][2] == subset2[i + 1][2])):
        subset2.pop(i + 1)
        my_len = my_len - 1

    i = i + 1
print("dates:")
print(subset2)

count = 0

plasma_temp_peaks = []
temp = []
decreasing_temp_patterns = []
patterns = []
final_proportions = []

for i in plasma_temp_peaks_indexes:
    plasma_temp_peaks.append(plasma_temp[i])

for i in range(len(plasma_temp_peaks) - 1):
    # Checking if there is a decreasing pattern
    if plasma_temp_peaks[i] == 368565.0:
        print()

    q1 = (plasma_temp_peaks[i] * 0.90) > plasma_temp_peaks[i - 1]
    q2 = (
            np.where(plasma_temp == plasma_temp_peaks[i])[0][0] - np.where(plasma_temp == plasma_temp_peaks[i - 1])[0][
        0]) > 48
    if q1 or q2:
        # If yes we add all the values in this pattern to the two-dimensional array and
        # make temp empty
        count += 1
        decreasing_temp_patterns.append(temp)
        temp = []
        temp.append(plasma_temp_peaks[i])
    else:
        # If not, then we add this temperature peak to the array
        temp.append(plasma_temp_peaks[i])

for i in decreasing_temp_patterns:
    if i:
        flag = True
        c = i[0]
        t = np.where(plasma_temp == i[0])[0][0]
        proportions = [c]
        for j in i:
            if ((np.where(plasma_temp == j)[0][0] - t) ** (1 / 3)) == 0:
                continue
            proportion = c // ((np.where(plasma_temp == j)[0][0] - t) ** (1 / 3)) + 30000
            proportions.append(proportion)
            if not ((proportion * 0.9) < j < (proportion * 1.1)):
                flag = False
        if flag:
            final_proportions.append(i)
        patterns.append(proportions)

print("Subset 2:")
print(subset2)
print()
print("Peaks:")
print(plasma_temp_peaks)
print()
print("Patterns:")
print(decreasing_temp_patterns)
print()
print(patterns)
print()
print("Result:")
print(final_proportions)

# print()
# print()
# print("PlASMA TEMP:")
# print(plasma_temp)
# print("PROTON DENSITY:")
# print(proton_density)
# print("PLASMA SPEED")
# print(plasma_speed)
