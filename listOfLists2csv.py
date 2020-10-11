import csv
import numpy as np

my_data = []

for i in range(1,91):
    a = np.load('coordinates_output_'+str(i)+'.npy')
    my_data.append(a[0])

with open("train.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(my_data)
