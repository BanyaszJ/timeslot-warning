from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from datetime import datetime, date, timedelta
from time import sleep as Sleep

import config
# import pprint


#====================== GLOBALS ===========================================
timeslotFound = False
DEBUG = False
#====================== SUPPORTING FUNCTIONS ===========================================

def path_exists(id, path):

    try:        
        if id == "id": driver.find_element_by_id(path)
        elif id == "text": driver.find_element_by_partial_link_text(path)
    except NoSuchElementException:
        return False
    return True
    

def wait_for(id, path):

    print "Loading page..."
    iteration = 1
    while not path_exists(id, path):
        Sleep(1)
        print "Waiting for page to load... (%s)" % iteration
        iteration += 1
        
        
def create_week_list():
    
    dt           = date.today()
    element_list = []

    for i in range(3):
        dt      = date.today()
        day     = dt + timedelta(days=i*7)
        month   = day.strftime("%B")[:3]
        day     = day.strftime("%d")
        str     = month + " " + day
        element_list.append(str)
        
    return element_list
        
        
def lookForTimeslot():
    print "Scraping page for available timeslots..."
    try: 
        driver.find_element_by_class_name('button.button-secondary.small.available-slot--button')
        driver.find_element_by_class_name('button.button-secondary.small.available-slot--button').click()
    except NoSuchElementException: 
        print "No slots available!\n"
        return False
    print "Available timeslot found..."
    return True
       
       
#=======================================================================================

driver = webdriver.Chrome(config.webdriver_path)
driver.get(config.start_page)
week_list = create_week_list()

print("=== LOADING: Login page ===")
wait_for('id', 'email')
driver.find_element_by_id("email").send_keys(config.my_email)
driver.find_element_by_id ("password").send_keys(config.my_password)
driver.find_element_by_class_name('smart-submit-button').click()

print("=== LOADING: Timeslots page ===")
wait_for('text', 'Book a slot')
driver.find_element_by_partial_link_text('Book a slot').click()

if DEBUG == True:
    wait_for('text', 'Click+Collect')
    driver.find_element_by_partial_link_text('Click+Collect').click()
elif DEBUG == False:
    wait_for('text', 'Home Delivery')
    driver.find_element_by_partial_link_text('Home Delivery').click()


driver.implicitly_wait(5)

iterweeks = 0
while not timeslotFound:
    driver.refresh()
    print("Refreshing timeslot page.")
    for week in week_list:
        wait_for('text', week)
        Sleep(1)
        print "Clicking link: %s ... (%s)" % (week, iterweeks)
        driver.find_element_by_partial_link_text('%s'% (week)).click()
        timeslotFound = lookForTimeslot()
        
        if timeslotFound: break    
        iterweeks += 1
        
driver.execute_script("window.open('https://www.youtube.com/watch?v=sJRVF-NCPVU');")   # VICTORY
print "====== TIMESLOT FOUND in %s interval!!! ======\n" % week