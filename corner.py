# coding=utf-8
import numpy as np
import os, sys, math, cv2
from os.path import join
import matplotlib.pyplot as mp

cityname = sys.argv[1]
maplevel = sys.argv[2]

road_bone_path = join('picture', '{0}-{1}-bone.png'.format(cityname, maplevel))
road_corner_path = join('picture', '{0}-{1}-corner.png'.format(cityname, maplevel))
road_simplfied_path = join('picture', '{0}-{1}-simplified.png'.format(cityname, maplevel))

pixel_path = join('pixel', '{0}-{1}.txt'.format(cityname, maplevel))
pixel_simplified_path = join('pixel', '{0}-{1}-simplified.txt'.format(cityname, maplevel))


img = cv2.imread(road_bone_path)
W, H, _ = img.shape
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
img = np.float32(img)
corner = cv2.cornerHarris(img, 4, 5, 0.05)
cv2.imwrite(road_corner_path, corner)
corner = np.round(cv2.imread(road_corner_path)/255).astype(bool)
corner = corner[:, :, 0] * corner[:, :, 1] * corner[:, :, 2]


with open(pixel_path, 'r') as fid:
	with open(pixel_simplified_path, 'w') as fid2:
		fid2.write('0 0 ' + str(np.shape(corner)[0] - 1) + ' 0 ' + str(np.shape(corner)[0] - 1) + ' ' + str(np.shape(corner)[1] - 1) + ' 0 ' + str(np.shape(corner)[1] - 1) + ' ')
		data = fid.read()[:-1].split('\n')
		for line in data[1:]:
			line = [int(each) for each in line.split(' ')]
			r = line[0::2]
			c = line[1::2]
			first = []
			string = ''
			for iter in range(len(r)):
				if corner[r[iter] - 1, c[iter] - 1]:
					if first == []:
						first = [r[iter] - 1, c[iter] - 1]
					string = string + str(r[iter] - 1) + ' ' + str(c[iter] - 1) + ' '
			if string:
				string = string + str(first[0]) + ' ' + str(first[1]) + '\n'
				fid2.write(string)


with open(pixel_path, 'r') as fid:
	with open(pixel_simplified_path, 'r') as fid2:
		fig = mp.figure(figsize=(20,20*H/W))
		ax = fig.add_subplot(111)
		ax.set_aspect(1.0, 'datalim')
		mp.axis('off')
		data = fid2.read()[0:-1].split('\n')
		for line in data:
			line = [int(each) for each in line.split(' ')]
			r = line[0::2]
			c = line[1::2]
			ax.plot(c, H-np.array(r), 'r')
		data = fid.read()[0:-1].split('\n')
		for line in data:
			line = [int(each) for each in line.split(' ')]
			r = [each - 1 for each in line[0::2]]
			c = [each - 1 for each in line[1::2]]
			ax.plot(c, H-np.array(r), 'b')
	fig.savefig(road_simplfied_path)