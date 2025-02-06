from time import sleep
import re
from playwright.sync_api import sync_playwright
from random import uniform
import random
import csv
from datetime import datetime

def get_random_user_agent():
	user_agents = [
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
	]
	return random.choice(user_agents)

def human_like_scroll(page):
	# Simulate human-like scrolling
	page.mouse.move(random.randint(100, 600), random.randint(100, 600))
	for _ in range(3):
		page.mouse.wheel(0, random.randint(300, 700))
		sleep(uniform(0.5, 1.5))

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
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	filename = f"google_places_{timestamp}.csv"
	
	# Create and open CSV file with headers
	with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
		fieldnames = ['Name', 'Rating', 'Reviews', 'Address', 'Phone', 'Website', 'Profiles']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		
		with sync_playwright() as p:
			# Create browser context with more human-like characteristics
			browser = p.chromium.launch(
				headless=False,
				args=[
					'--disable-blink-features=AutomationControlled',
					'--disable-features=IsolateOrigins,site-per-process',
				]
			)
			
			context = browser.new_context(
				user_agent=get_random_user_agent(),
				viewport={'width': 1920, 'height': 1080},
				geolocation={'latitude': 40.7128, 'longitude': -74.0060},  # NYC coordinates
				permissions=['geolocation'],
				timezone_id='America/New_York',
				locale='en-US',
				java_script_enabled=True,
			)

			# Add human-like browser properties
			context.add_init_script("""
				Object.defineProperty(navigator, 'webdriver', {
					get: () => undefined
				});
				Object.defineProperty(navigator, 'plugins', {
					get: () => [1, 2, 3, 4, 5]
				});
			""")

			page = context.new_page()
			
			# Add random delays between actions
			page.set_default_timeout(30000)
			
			# Navigate to Google with random timing
			page.goto(f"https://www.google.com/search?q={query}")
			sleep(uniform(2, 4))
			
			# Simulate human-like behavior before clicking
			human_like_scroll(page)
			
			# Try to find and click "More places" with different strategies
			try:
				# Wait randomly before clicking
				sleep(uniform(1, 2))
				more_places_selectors = [
					"text='More places'",
					"text='Show more'",
					"//span[contains(text(), 'More places')]",
					"//div[contains(text(), 'More places')]"
				]
				
				for selector in more_places_selectors:
					try:
						page.click(selector, timeout=5000)
						break
					except:
						continue
					
			except Exception as e:
				print(f"Could not find 'More places' button: {e}")
				return None

			page_count = 0
			while True:
				# Add random delays between page loads
				sleep(uniform(2, 4))
				
				# Simulate human scrolling
				human_like_scroll(page)
				
				try:
					# Wait for business headings to load
					page.wait_for_selector('[role="heading"][aria-level="3"]')
					business_headings = page.query_selector_all('[role="heading"][aria-level="3"]')

					for heading in business_headings:
						try:
							# Get heading text
							heading_text = heading.inner_text()
							if not heading_text:
								continue
							
							# Click to open the business details
							heading.click()
							sleep(uniform(1, 2))
							
							# Wait for dialog to appear
							page.wait_for_selector('.xpdopen')
							
							# Extract data from the card
							card = page.query_selector('.xpdopen')
							if card:
								# Use more specific selectors
								name = heading_text
								
								rating_elem = card.query_selector('g-review-stars')
								rating = rating_elem.query_selector('span').get_attribute('aria-label').replace(" out of 5,", "").replace("Rated ", "") if rating_elem else "Not Found!"

								reviews_elem = card.query_selector(f'[aria-label="Rated {rating} out of 5,"] + *')
								reviews = reviews_elem.inner_text().strip('()') if reviews_elem else "0"
								
								address_elem = card.query_selector('[data-attrid="kc:/location/location:address"] .LrzXr')
								address = address_elem.inner_text() if address_elem else "Not Found!"
								
								phone_elem = card.query_selector('[ssk="14:4_local_action"]')
								phone = phone_elem.query_selector('a').get_attribute('data-phone-number') if phone_elem else "Not Found!"
								print(phone)
								
								website_elem = card.query_selector('[ssk="14:0_local_action"]')
								website = website_elem.query_selector('a').get_attribute('href') if website_elem else "Not Found!"
								print(website)
								profiles = []
								profiles_section = card.query_selector_all('g-link')
								for profile in profiles_section:
									profiles.append(profile.query_selector('a').get_attribute('href'))
								
								# Write row immediately to CSV
								writer.writerow({
									'Name': name,
									'Rating': rating,
									'Reviews': reviews,
									'Address': address,
									'Phone': phone,
									'Website': website,
									'Profiles': '; '.join(profiles)
								})
								csvfile.flush()  # Ensure data is written
								# Close card
								sleep(uniform(1, 2))
						except Exception as e:
							if e != SystemExit:
								print(f"Error processing place: {e}")
								continue
					# Random delay before trying next page
					sleep(uniform(3, 5))
					
					# Try to click next page with human-like behavior
					next_button = page.query_selector('#pnnext')
					if not next_button:
						break
					
					# Move mouse naturally to the next button
					page.mouse.move(
						random.randint(0, 20),
						random.randint(0, 20)
					)
					next_button.click()
					page_count += 1
					
					# Random longer delay between pages
					sleep(uniform(5,10))
					
				except Exception as e:
					print(f"Error on page {page_count}: {e}")
					break

			# Clean up
			context.close()
			browser.close()

	if not filename:
		print("No results found!")
		return None

	return filename

if __name__ == "__main__":
	output_file = scrape("Beauty Salons in New York City")
	if output_file:
		print(f"Results saved to: {output_file}")