from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, sys, time, json
from os.path import join
from tqdm import tqdm

cityname = sys.argv[1]
maplevel = int(sys.argv[2])
use_simplified = True

dpi_path = join('dpi', '{}.json'.format(cityname))
if use_simplified:
	pixel_path = join('pixel', '{0}-{1}-simplified.txt'.format(cityname, maplevel))
	coor_path = join('coor', '{0}-{1}-simplified.json'.format(cityname, maplevel))
else:
	pixel_path = join('pixel', '{0}-{1}.txt'.format(cityname, maplevel))
	coor_path = join('coor', '{0}-{1}.json'.format(cityname, maplevel))
	
with open(dpi_path, 'r') as f:
	dpi = json.load(f)
	left, up = dpi[:2]
	
# enable browser logging
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities['goog:loggingPrefs'] = { 'browser':'ALL' }

options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
options.add_argument('headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(executable_path='./chromedriver.exe', desired_capabilities=desired_capabilities, options=options)
driver.delete_all_cookies()

url = 'file:///' + os.path.abspath('HTML/pixel2coor.html')
print(url)
driver.get(url)
driver.get_log('browser')

coor = []
with open(pixel_path, 'r') as f:
	pixel = f.read()[:-1].split('\n')
	bar = tqdm(range(len(pixel)), ncols=50)
	for iter in bar:
		pixel[iter] = pixel[iter].split(' ')
		coor.append([])
		for iter2 in range(0, len(pixel[iter]), 2):
			bar.set_description('{0} / {1}'.format(iter2 // 2, len(pixel[iter]) // 2))
			x = left + (float(pixel[iter][iter2]) - 500) * (2 ** (18 - maplevel))
			y = up - (float(pixel[iter][iter2 + 1]) - 500) * (2 ** (18 - maplevel))
			driver.find_element_by_name("pixel").send_keys('{0} {1}'.format(x, y))
			driver.find_element_by_name("button").click()
		
		logs = driver.get_log('browser')
		for iter2 in logs:
			iter2 = iter2['message'].replace('\"', '').split(' ')
			coor[-1].append([float(iter2[-2]), float(iter2[-1])])
		with open(coor_path, 'w') as f:
			json.dump(coor, f)
driver.quit()