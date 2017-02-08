# Thanks to https://github.com/jenkin
# This script is a modified version of: https://github.com/jenkin/scraping-mastersportaleu
# it's way more structured and clean then Selenium's version

### THIS CODE IS FOR EXPERIMENTAL PURPOSES ONLY, DON'T USE IT!!!

import requests, csv, re, time
from bs4 import BeautifulSoup as bs

main_url = "http://www.mastersportal.eu/countries/"
countries_res = requests.get(main_url)
countries_page = bs(countries_res.text,"lxml")

countries_headers = ["url","name","id"]
countries_file = open("countries.csv","a")
countries_csv = csv.DictWriter(countries_file, fieldnames = countries_headers)
countries_csv.writeheader()

universities_headers = ["url","name","id","country"]
universities_file = open("universities.csv","a")
universities_csv = csv.DictWriter(universities_file, fieldnames = universities_headers)
universities_csv.writeheader()

studies_headers = ["url","name","id","university","country"]
studies_file = open("studies.csv","a")
studies_csv = csv.DictWriter(studies_file, fieldnames = studies_headers)
studies_csv.writeheader()

details_headers = ["url_course","course", "id", "uni", "fees", "duration", "university", "country"]
details_file = open("details.csv","a")
details_csv = csv.DictWriter(details_file, fieldnames = details_headers)
details_csv.writeheader()

for c in countries_page.select("#CountryOverview li a"):

	country_url = c['href'].encode('utf8')
	country_name = c['title'].encode('utf8')
	country_id = re.search("/\d+/",country_url).group()[1:-1]

	print "+", country_name, "("+country_id+")"

	countries_csv.writerow({
	"url": country_url.replace(",",""),
	"name": country_name.replace(",",""),
	"id": country_id.replace(",","")
	})

	universities_res = requests.get(country_url)
	universities_page = bs(universities_res.text,"lxml")

	time.sleep(4)

	for u in universities_page.select("#CountryStudies li a"):

		university_url = u['href'].encode('utf8')
		university_name = u['title'].encode('utf8')
		university_id = re.search("/\d+/",university_url).group()[1:-1]
		university_country = country_id

		print "++", university_name, "("+university_id+")"

		universities_csv.writerow({
				"url": university_url.replace(",",""),
				"name": university_name.replace(",",""),
				"id": university_id.replace(",",""),
				"country": university_country.replace(",","")
				})

		studies_res = requests.get(university_url)
		studies_page = bs(studies_res.text,"lxml")

		time.sleep(3)

		for s in studies_page.select("#StudyListing .StudyInfo a"):
			study_url = s['href'].encode('utf8')
			study_name = s['title'].encode('utf8')
			study_id = re.search("/\d+/",study_url).group()[1:-1]
			study_university = university_id
			study_country = country_id

			print "+++", study_name, "("+study_id+")"
			
			try:
				details_res = requests.get(study_url)
				details_page = bs(details_res.text,"lxml")
				time.sleep(1)
				price = details_page.find("span", class_="Amount")
				duration = details_page.find("abbr", class_="Duration FactData")
				clean_price = ""
				clean_duration = ""

				def cleanprice(x):
					global clean_price
					if x != None:
						clean_price = x.text.encode('utf-8')
					else:
						clean_price = "N/A"

				def cleanduration(x):
					global clean_duration
					if x != None:
						clean_duration = x.text.encode('utf-8')
					else:
						clean_duration = "N/A"

				cleanprice(price)
				cleanduration(duration)
				#credits = details_page.find("div", class_="FactData Credits").text
				details_csv.writerow({
						"url_course": study_url.replace(",",""),
						"course": study_name.replace(",",""),
						"id": study_id.replace(",",""),
						"uni": university_name.replace(",",""),
						"fees": clean_price.replace(",",""),
						"duration": clean_duration.replace(",",""),
						"university": university_id.replace(",",""),
						"country": country_name.replace(",","")
						#"credits": credits.replace(",","")
						})
			except Exception as e:
				print e
				time.sleep(5)

	time.sleep(2)

countries_file.close()
universities_file.close()
studies_file.close()
