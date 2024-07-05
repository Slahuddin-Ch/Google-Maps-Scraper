# Google-Maps-Scraper
This powerful Python script leverages the Playwright library to perform comprehensive web scraping and data extraction from Google Maps. Ideal for collecting detailed information about businesses, including their names, addresses, websites, phone numbers, reviews, and more.

## Table of Contents

- [Prerequisite](#prerequisite)
- [Key Features](#key-features)
- [Installation](#installation)
- [How to Use](#how-to-use)

## Prerequisite
- Python version below 3.10 is required. Versions beyond 3.9 may cause issues and may not work properly.

## Key Features
- **Data Scraping**: Extracts business names, addresses, websites, and contact details from Google Maps listings.
- **Review Analysis**: Gathers review counts and average ratings, offering insights into businesses' online reputations.
- **Business Type Detection**: Identifies whether a business offers in-store shopping, in-store pickup, or delivery services.
- **Operating Hours**: Extracts detailed information about business operating hours.
- **Introduction Extraction**: Scrapes introductory information about businesses when available.
- **Data Cleansing**: Cleanses and organizes scraped data, removing redundant or unnecessary columns.
- **CSV Export**: Exports cleaned data to a CSV file for further analysis or integration with other tools.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/zohaibbashir/google-maps-scraping.git
   ```

2. Navigate to the project directory:
   ```bash
   cd google-maps-scraping
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use

1. Run the script with Python:
   ```bash
   python main.py -s "search term" -t total
   ```
   Replace "search term" with the name of the place/business and "total" with the number of listings you want to scrape. For example:
   ```bash
   python main.py -s "Turkish Restaurants in Toronto Canada" -t 20
   ```

2. The script will launch a browser, perform the search, and start scraping information. Progress will be displayed, and results will be saved to a CSV file named `result.csv`.

## Example Use Cases
- **Market Research**: Gather data on competitors and market trends.
- **Lead Generation**: Extract contact information for potential business leads.
- **Reputation Management**: Analyze online reviews to assess business reputation.
- **Operational Analysis**: Study operating hours and service types of similar businesses.

## Future Enhancements
- **Automated Data Updates**: Implement scheduled scraping to keep data up-to-date.
- **Enhanced Data Visualization**: Integrate visualization tools for deeper insights.
- **Geo-Location Filtering**: Add features to filter results by specific geographic regions.
- **Multi-Language Support**: Expand capabilities to support multiple languages.

Unlock the full potential of Google Maps data with the Google-Maps-Scraper. Whether for market research, lead generation, or reputation management, this tool provides invaluable insights and data at your fingertips.