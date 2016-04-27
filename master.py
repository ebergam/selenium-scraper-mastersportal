#THE PURPOSE OF THIS PROJECT IS ONLY EXPERIMENTAL! DON'T USE IT!

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv

driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("http://www.mastersportal.eu/search/?q=di-4|ln-3,7|lv-master|rv-1|tx-20000|tt-eea|tu-year&order=name&direction=asc")
scroll = driver.find_element_by_tag_name('html')

list_of_names = []
list_of_places = []
list_of_unis = []
list_of_costs = []

#the range is set with the number of pages you can see on the website, but one could automate this by scraping the number
for x in range(0, 66):
	page_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "icon-arrow-right2-after")))
	containers = driver.find_elements_by_xpath("//*[@id='StudySearchResultsStudies']/div[1]")
	for item in containers:
		names = driver.find_elements_by_xpath("//div[@id='StudySearchResultsStudies']/div/h3/a")
		for item in names:
		    list_of_names.append(item.text.encode('utf-8'))

		places = driver.find_elements_by_xpath("//*[@id='StudySearchResultsStudies']/div/div[2]/div/ul[2]/li")
		for item in places:
		    list_of_places.append(item.text.encode('utf-8'))

		unis = driver.find_elements_by_xpath("//div[@id='StudySearchResultsStudies']/div/div[2]/div/ul[1]/li/a")
		for item in unis:
		    list_of_unis.append(item.text.encode('utf-8'))

		costs = driver.find_elements_by_class_name("eea")
		for item in costs:
		    list_of_costs.append(item.text.encode('utf-8'))
	 
	scroll.send_keys(Keys.END)
	time.sleep(1)
	page_button.click()

list_of_lists = [list_of_names, list_of_places, list_of_unis, list_of_costs]

#An alternative method to click on the 'next button' by injecting JS. Not tested
#driver.execute_script("var arrow = document.getElementsByClassName('icon-arrow-right2-after'); arrow.click();");

#It prints the list to terminal 
#print list_of_lists

outfile = open("./results.csv", "wb")
writer = csv.writer(outfile)
writer.writerows(list_of_lists)

#for readabilty you'll need to pivot the csv (transform rows into columns). There are plenty of online tools to do so

#It closes the browser when finished
#driver.quit()
