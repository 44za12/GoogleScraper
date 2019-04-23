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
options.binary_location = '/app/.apt/usr/bin/google-chrome'
driver = webdriver.Chrome('/app/.chromedriver/bin/chromedriver',options=options)
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
	body = str(body)
	phone = cleanhtml(body)
	phone = phone.replace(" ","")
	return phone
def scrape(query):
	results = []
	query = query.replace(" ","+")
	google = "https://www.google.com"
	url = google+"/search?q="+query
	driver.get(url)
	driver.find_elements_by_xpath("//span[contains(text(), 'More places')]")[0].click()
	places = driver.find_elements_by_xpath('//a[@role="link"]')
	for i in places:
		place = {}
		n = i.get_attribute('innerHTML')
		temp = re.findall(r'<div>(.*?)</div>',n)
		place['Name'] = getName(temp[0])
		place['Stars'] = getStars(temp[1])
		place['Reviews'] = getReviewCount(temp[1])
		place['Location'] = getLocation(temp[2])
		place['Phone'] = getPhone(temp[3])
		results.append(place)
	for y in range(2,3):
		z = 0
		driver.find_element_by_xpath('//a[@class="pn"]').click()
		places = driver.find_elements_by_xpath('//a[@role="link"]')
		for i in places:
			place = {}
			n = i.get_attribute('innerHTML')
			temp = re.findall(r'<div>(.*?)</div>',n)
			place['Name'] = getName(temp[0])
			place['Stars'] = getStars(temp[1])
			place['Reviews'] = getReviewCount(temp[1])
			place['Location'] = getLocation(temp[2])
			place['Phone'] = getPhone(temp[3])
			results.append(place)
		sleep(5)
	header = results[0].keys()
	t = DataFrame(results)
	filename = "gs"+str(randint(0,2324))+".xlsx"
	writer = ExcelWriter(filename, engine='xlsxwriter')
	t.to_excel(writer,'Sheet1', encoding='utf-8', index=False, columns=header)
	writer.save()
	return filename
scrape("Salons in Delhi")