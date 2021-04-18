import selenium
import getpass
from urllib2 import Request, urlopen, URLError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

inputUser = raw_input('Please enter your Alma admin username: ')
if inputUser.lower() != '':
    print('Valid username.')
else:
    print('Invalid username.')
    exit()

inputPassword = getpass.getpass(prompt='Please enter your Alma admin password: ')
if inputPassword.lower() != '':
    print('Valid password.')
else:
    print('Invalid password.')
    exit()

url = raw_input('Please enter your Alma subdomain for the school portal: ')

loginPage = "https://" + str(url) + ".getalma.com/"
req = Request(loginPage)
try:
    response = urlopen(req)
except URLError, e:
    if hasattr(e, 'reason'):
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        exit()
    elif hasattr(e, 'code'):
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        exit()
else:
    print 'Portal is valid!'

student = loginPage + "student/"
fileCabinet = "/file-cabinet"

# Creates link list array singly linked list.
almaID = []
with open('/home/perfectdotexe/Desktop/list.txt','r') as f: 
    for i in f:
        almaID.append(i.strip())

finalList = student + str(almaID).strip("['']") + fileCabinet

driver = webdriver.Firefox()
driver.get(loginPage)

u = driver.find_element_by_name('username')
u.send_keys(inputUser)
p = driver.find_element_by_name('password')
p.send_keys(inputPassword)
p.send_keys(Keys.RETURN)

# Waits for login (3 seconds)
delay = 3

# Tests for element ID, ui-home-index which is only accessible by logging in then moves to scraping.
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'ui-home-index')))
    driver.get(finalList)
    driver.implicitly_wait(3)
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        print(elem.get_attribute("href"))
    
    # Will throw error if login is incorrect
except TimeoutException:
    print "Loading took too much time!"