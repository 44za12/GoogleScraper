# GoogleScraper
A modern Google Places scraper that works without the Google Places API. Extracts business information including names, ratings, reviews, contact details, and social profiles.

## Features
- No API key required
- Extracts comprehensive business data:
  - Business name
  - Rating and review count
  - Address
  - Phone number
  - Website
  - Social media profiles
- Human-like behavior to avoid detection
- Results saved to CSV format
- Built with Playwright for reliable web automation

## Installation
1. Clone the repository:
```bash
git clone https://github.com/44za12/GoogleScraper.git
cd GoogleScraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```


3. Install Playwright browsers:
```bash
playwright install
```

4. Change the query in the GoogleScraper.py file

5. Run the scraper:
```bash
python GoogleScraper.py
```

The script will save results to a timestamped CSV file (e.g., `google_places_20240312_143022.csv`)

## Example Output
The CSV file will contain the following columns:
- Name: Business name
- Rating: Customer rating (out of 5)
- Reviews: Number of reviews
- Address: Physical location
- Phone: Contact number
- Website: Business website
- Profiles: Social media and other web profiles

## Notes
- Uses random delays and human-like behavior to avoid detection
- For educational purposes only

## Requirements
- Python 3.10+
- Playwright
- Other dependencies listed in requirements.txt