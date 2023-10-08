import numpy as np
import sys
from scipy.signal import find_peaks

dataset = np.loadtxt("datasets/omniweb.gsfc.nasa.gov_staging_omni2_kJq2CCn1rj.lst (1).txt",
                     dtype=float)

np.set_printoptions(suppress=True)
np.set_printoptions(threshold=sys.maxsize)

plasma_temp = dataset[:, 11]
proton_density = dataset[:, 12]
plasma_speed = dataset[:, 13]

plasma_temp_peaks, _ = find_peaks(plasma_temp, distance=150)
proton_density_peaks, _ = find_peaks(proton_density, distance=150)
plasma_speed_peaks, _ = find_peaks(plasma_speed, distance=150)
print(plasma_temp_peaks)
print(proton_density_peaks)
print(plasma_speed_peaks)

final_j = 0
final_i = 0
final_k = 0

subset1 = []

# idk how this works tbh
for i in range(len(plasma_temp_peaks)):
    subset1.append([plasma_temp_peaks[i]])
    for j in range(len(proton_density_peaks)):
        if (abs(subset1[i][0] - proton_density_peaks[j]) < 72):
            subset1[i].append(proton_density_peaks[j])

for j in range(len(subset1)):
    subset1[j].append(72 - abs(subset1[j][0] - subset1[j][1]))

subset2 = []
for i in range(len(subset1)):
    for j in range(len(plasma_speed_peaks)):
        if (abs(subset1[i][0] - plasma_speed_peaks[j]) < subset1[i][2]):
            subset2.append([subset1[i][0], subset1[i][1], plasma_speed_peaks[j]])
        if (abs(subset1[i][1] - plasma_speed_peaks[j]) < subset1[i][2]):
            subset2.append([subset1[i][0], subset1[i][1], plasma_speed_peaks[j]])

my_len = len(subset2) - 1
i = 0
while (i < my_len):
    if ((subset2[i][0] == subset2[i + 1][0]) and (subset2[i][1] == subset2[i + 1][1]) and (
            subset2[i][2] == subset2[i + 1][2])):
        subset2.pop(i + 1)
        my_len = my_len - 1

    i = i + 1
print(subset2)

print(plasma_temp, proton_density, plasma_speed)