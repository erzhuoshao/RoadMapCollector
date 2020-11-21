from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, sys, time, json

cityname = sys.argv[1]

# enable browser logging
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities['goog:loggingPrefs'] = { 'browser':'ALL' }

options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
options.add_argument('headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(executable_path='./chromedriver.exe', desired_capabilities=desired_capabilities, options=options)
driver.delete_all_cookies()
url = 'file:///' + os.path.abspath('HTML/getbound.html') + '?' + cityname
driver.get(url)
print(url)
time.sleep(3)

# The format of this line is not changeable for unknown reason !!!
# Or logs would only contain the first line of console.log()
logs = [log for log in driver.get_log('browser')]
driver.quit()

bound = logs[-1]['message'].split(' \"')[1][:-1]
bound = [tuple([float(iter2) for iter2 in iter.split(', ')]) for iter in bound.split(';')]
with open('bound/{}.json'.format(cityname), 'w') as f:
	json.dump(bound, f)