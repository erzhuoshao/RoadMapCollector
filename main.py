# coding=utf-8
import math, os, random, json, sys, retry, time
from os.path import join
import numpy as np
from PIL import Image
from selenium import webdriver
from tqdm import tqdm

#@retry.retry(tries=10, delay=1 + random.random() * 2)
def get(driver, url, log=''):
	driver.get('about:blank')
	if(log):
		print(log)
	driver.get(url)

def getbound(cityname):
	path = 'bound/{}.json'.format(cityname)
	if not os.path.exists(path):
		os.system('python HTML/getbound.py {}'.format(cityname))
	with open(path, 'r') as f:
		return np.array(json.load(f))

# get the pixel_lonlat transformation dpi
def getdpi(cityname, maplevel, points):
	path = 'dpi/{}.json'.format(cityname)
	if not os.path.exists(path):
		os.system('python HTML/getdpi.py {0} {1} {2} {3} {4}'.format(cityname, *points))
	with open(path, 'r') as f:
		pixels = np.array(json.load(f)) # Read the Leftup and Rightdown points
	# left, up, right, down
	lon_div_pix = np.abs((points[0] - points[2])/(pixels[0] - pixels[2]))
	lat_div_pix = np.abs((points[1] - points[3])/(pixels[1] - pixels[3]))
	
	# Scaling dpi by maplevel, 18 is the finest maplevel
	lon_div_pix *= (2 ** (18 - int(maplevel)))
	lat_div_pix *= (2 ** (18 - int(maplevel)))
	return lon_div_pix, lat_div_pix


# call chrome to capture screen and record the pixel-lonlat list
def callscreen(driver, path_dict, left, up, width, height):
	waiting_time = 1 # second, should be changed according to connecting condition
	patchDirPath = path_dict['patchDirPath']
	delta = path_dict['delta']
	
	for i in range(width):
		for j in range(height):
			patchPath = join(patchDirPath, '{0}-{1}.png'.format(i, j))
			if not os.path.exists(patchPath):
				count = 5
				while count > 0:
					url = 'file:///' + os.path.abspath('HTML/getpatch.html')
					url += '?{0}&{1}&{2}&{3}&{4}&{5}'.format(left, up, - i * delta, - j * delta, maplevel, 'off')
					print(url)
					get(driver, url, 'try to download:{0}/{1}-{2}/{3}'.format(i,width,j,height))
					time.sleep(waiting_time)
					driver.get_screenshot_as_file(patchPath)
					get(driver, 'about:blank')
					if os.path.exists(patchPath):
						d = np.array(Image.open(patchPath))
						if d.sum() == 0:
							print('Image collection failed : {0}/{1}-{2}/{3}'.format(i, width, j, height))
							count -= 1
							continue
						else:
							print('Successfully downloaded : {0}/{1}-{2}/{3}'.format(i, width, j, height))
							print(patchPath)
							break
					else:
						count -= 1
			else:
				print('File already exists : {0}/{1}-{2}/{3}'.format(i, width, j, height))



def core(driver, path_dict):
	cityname = path_dict['cityname']
	maplevel = path_dict['maplevel']
	delta = path_dict['delta']
	picturePath = path_dict['picturePath']
	patchDirPath = path_dict['patchDirPath']

	bound = getbound(cityname)
	left, up, right, down = min(bound[:, 0]), max(bound[:, 1]), max(bound[:, 0]), min(bound[:, 1])
	print('left, up, right, down == {}'.format([left, up, right, down]))
	
	dpi_w, dpi_h = getdpi(cityname, maplevel, [left, up, right, down])
	print('dpi_w, dpi_h = {0:.8f}, {1:.8f}'.format(dpi_w, dpi_h))

	width = int(math.ceil(abs(left - right) / (dpi_w * delta)))
	height = int(math.ceil(abs(up - down) / (dpi_h * delta)))
	
	print('Collecting Patches....')
	callscreen(driver, path_dict, left, up, width, height)
	
	print('Pasting Patches....')
	pathlist = os.listdir(patchDirPath)
	image = Image.new('RGB', (width * delta, height * delta))
	for line in tqdm(pathlist):
		data = Image.open(join(patchDirPath, line)).resize([delta, delta])
		data = data.convert('RGB')
		id = line.split('.')[0].split('-')
		x, y = int(id[0]) * delta, int(id[1]) * delta
		image.paste(data, (x, y))
	print('Saving Picture....')
	image.save(picturePath)


if __name__ == '__main__':
	debug_mode = True
	cityname = sys.argv[1]
	maplevel = sys.argv[2]
	delta = 1000 # Patch's size
	
	path_dict = {
		'cityname' : cityname,
		'maplevel' : maplevel,
		'delta' : delta,
		'picturePath' : join('picture', '{0}-{1}.png'.format(cityname, maplevel)),
		'patchDirPath' : join('patch', '{0}-{1}'.format(cityname, maplevel)),
	}

	if not os.path.isdir(path_dict['patchDirPath']):
		os.makedirs(path_dict['patchDirPath'])
		
	option = webdriver.ChromeOptions()
	option.add_argument('disable-infobars')
	option.add_argument('headless')

	driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=option)
	driver.delete_all_cookies()
	driver.set_window_size(delta, delta)
	driver.set_page_load_timeout(10)
	
	for iter in range(1):
		if debug_mode:
			core(driver, path_dict)
		else:
			try:
				core(driver, path_dict)
			except:
				pass
			
