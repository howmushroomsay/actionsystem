import sys
import os
dist_path = sys.argv[1]
for file in os.listdir(dist_path):
    if file[0:2] == 'Qt' and file[-3:] == 'dll':
        os.remove(os.path.join(dist_path, file))
