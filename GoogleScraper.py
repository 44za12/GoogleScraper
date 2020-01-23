from time import sleep
import re
from selenium import webdriver
from pandas import DataFrame
from pandas import ExcelWriter
from random import randint
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
# options.binary_location = '/app/.apt/usr/bin/google-chrome'
chromedriverpath = 'chrome_driver_path_here'
driver = webdriver.Chrome(chromedriverpath,options=options)
driver.implicitly_wait(15)
def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext
def getName(body):
	name = cleanhtml(body)
	return name
def getStars(body):
	body = str(body)
	stars = cleanhtml(body)
	try:
		stars = stars.split()
		stars = str(stars[0])+" Stars"
	except:
		stars = str(stars)+" Stars"
	return stars
def getReviewCount(body):
	body = str(body)
	reviews = cleanhtml(body)
	try:
		reviews = reviews.split()
		reviews = str(reviews[1])
		reviews = reviews.replace("(","")
		reviews = reviews.replace(")","")
		reviews = reviews+" Reviews"
	except:
		reviews = reviews
	return reviews
def getLocation(body):
	city = cleanhtml(body)
	try: 
		city = city.split(" · ")
		city = city[0]
	except:
		city = str(city[0])
	return city
def getPhone(body):
	try:
		body = str(body)
		phone = cleanhtml(body)
		phone = phone.split("·")
		try:
			phone = phone[2]
		except:
			try:
				phone = phone[1]
			except:
				phone = phone
	except:
		phone = "Not found!"
	phone = phone.replace(" ","")
	return phone
def scrape(query):
	results = []
	query = query.replace(" ","+")
	google = "https://www.google.com"
	url = google+"/search?q="+query
	driver.get(url)
	driver.find_elements_by_xpath("//span[contains(text(), 'More places')]")[0].click()
	for y in range(15):
		places = driver.find_elements_by_xpath('//a[@role="link"]')
		for i in places:
			place = {}
			n = i.get_attribute('innerHTML')
			temp = re.findall(r'<div>(.*?)</div>',n)
			place['Name'] = getName(temp[0])
			place['Stars'] = getStars(temp[1])
			place['Reviews'] = getReviewCount(temp[1])
			place['Location'] = getLocation(temp[2])
			try:
				place['Phone'] = getPhone(temp[3])
			except:
				place['Phone'] = "Not Found!"
			results.append(place)
		sleep(5)
		try:
			driver.find_element_by_xpath('//a[@id="pnnext"]').click()
		except:
			pass
	header = results[0].keys()
	t = DataFrame(results)
	filename = "gs"+str(randint(0,2324))+".xlsx"
	writer = ExcelWriter(filename, engine='xlsxwriter')
	t.sort_values("Phone", inplace=True) 
	t.drop_duplicates(keep=False, inplace=True)
	t.to_excel(writer,'Sheet1', encoding='utf-8', index=False, columns=header)
	writer.save()
	return filename