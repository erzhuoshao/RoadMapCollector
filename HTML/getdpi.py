from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, sys, logging, time, json
import pandas as pd

cityname, left, up, right, down = sys.argv[1:]

# enable browser logging
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities['goog:loggingPrefs'] = { 'browser':'ALL' }

options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
options.add_argument('headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(executable_path='./chromedriver.exe', desired_capabilities=desired_capabilities, options=options)
driver.delete_all_cookies()
url = 'file:///' + os.path.abspath('HTML/getdpi.html') + '?{0}&{1}&{2}&{3}'.format(left, up, right, down)
driver.get(url)
print(url)
time.sleep(3)

# The format of this line is not changeable for unknown reason !!!
# Or logs would only contain the first line of console.log()
logs = [log for log in driver.get_log('browser')]
driver.quit()

points = logs[-1]['message'].split(' \"')[1][:-1]
points = tuple([float(iter) for iter in points.split(',')])
with open('dpi/{}.json'.format(cityname), 'w') as f:
	json.dump(points, f)