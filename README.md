# selenium-scraper-mastersportal
A scraper in python's selenium for mastersportal.eu
THE PURPOSE OF THIS PROJECT IS ONLY EXPERIMENTAL! DON'T USE IT!

A guide-through the code:

After importing Selenium and the other instruments, we open the Firefox's webdriver and make a get request on the URL in which we're interested, previously obtained with a research.
Then we define the variable "scroll" which will be the whole HTML, so that we will exploit Selenium's SendKeys function, a powerful instrument to easily send any key to the browser, as if an actual user was pressing it.

	driver = webdriver.Firefox()
	driver.implicitly_wait(10)
	driver.get("http://www.mastersportal.eu/search/?q=di-4|ln-3,7|lv-master|rv-1|tx-20000|tt-eea|tu-year&order=name&direction=asc")
	scroll = driver.find_element_by_tag_name('html')

After that we create empty arrays that will contain the information we're interested in:

	list_of_names = []
	list_of_places = []
	list_of_unis = []
	list_of_costs = []

The next step is to create a nested loop. The first loop is used to automate the process of clicking 'next page'. We define page_button as the 'next' button. We need to use an implicit wait, in order to wait for the visibility of this element for the program to continue. Once the element is created in the DOM it's found by Class (this is why at the beginning we imported by exception). After executing the nested loops the page will scroll to the end, in order to make the button visible. We need to make it sleep for one second (you may wanna increase this value) because an element need to stay still on coordinates before clicking (if not, you may get the "element unclickable at position x,y" error). 

	for x in range(0, 66):
	page_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "icon-arrow-right2-after")))
	containers = driver.find_elements_by_xpath("//*[@id='StudySearchResultsStudies']/div[1]")

	#nested loops...

	scroll.send_keys(Keys.END)
	time.sleep(1)
	page_button.click()


Let's see what's in the nested loops. Before we defined the "containers" as all the spaces containing the information we're interested into, and we used a locating function working with XPATH, that returned a list. In the same way we loop through that list to find the names and all the other information. For every item of that, then, we append to the array the text encoded to 'utf-8'. We need the encoding as many names contain non-ascii letters (for example the italian Universit**à**)

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

Last step is to append all the lists to a list_of_lists (pretty self-explanatory). With Python's CSV functions we can create the outfile to be created with the data. These are horizontal strings, so it's totally convenient to transpose the CSV (exchange rows with columns). You can do it with an online tool such as [this](http://www.convertcsv.com/transpose-csv.htm)

	list_of_lists = [list_of_names, list_of_places, list_of_unis, list_of_costs]

	outfile = open("./results.csv", "wb")
	writer = csv.writer(outfile)
	writer.writerows(list_of_lists)
