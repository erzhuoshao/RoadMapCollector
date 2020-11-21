import os, sys, time, json
from os.path import join
from tqdm import tqdm
from coordTransform_utils import bd09_to_gcj02 # baidu coor to GuoCeJu

cityname = sys.argv[1]
maplevel = int(sys.argv[2])
use_simplified = True

if use_simplified:
	coor1_path = join('coor', '{0}-{1}-simplified.json'.format(cityname, maplevel))
	coor2_path = join('coor', '{0}-{1}-simplified-gcj.json'.format(cityname, maplevel))
else:
	coor1_path = join('coor', '{0}-{1}.json'.format(cityname, maplevel))
	coor2_path = join('coor', '{0}-{1}-gcj.json'.format(cityname, maplevel))
	
with open(coor1_path, 'r') as f:
	data = json.load(f)
	for iter in range(len(data)):
		for iter2 in range(len(data[iter])):
			data[iter][iter2] = bd09_to_gcj02(*data[iter][iter2])

with open(coor2_path, 'w') as f:
	json.dump(data, f)
