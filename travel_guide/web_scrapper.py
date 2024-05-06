# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Section names (modify as needed)
sections = [
    "Names and Titles", "Especially for Men", "Corporate Culture", "Gifts",
    "Dining and Entertainment", "Meeting and Greeting", "Especially for Women",
    "Body Language", "Dress", "Regional Differences", "Helpful Hints",
    "American Women", "Language"
]

# Function to scrape data from a country detail page
def scrape_country_detail(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")

  # Compile data for each section
  country_data = {}
  current_section = None
  for element in soup.find_all(True):
    if element.name == "p" and element.has_attr("class") and "mainhead" in element["class"]:
      current_section = element.get_text(strip=True)
      country_data[current_section] = []
    elif current_section and (element.name == "p" or element.name == "li"):
      country_data[current_section].append(element.get_text(strip=True))

  # Filter data for requested sections
  return {section: details for section, details in country_data.items() if section in sections}

# Base URL and main URL
base_url = "http://www.ediplomat.com/np/cultural_etiquette/"
main_url = base_url + "cultural_etiquette.htm"

# Get response and soup for main page
response = requests.get(main_url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all tables containing country lists
tables = soup.find_all("table")

# Extract country names and URLs
country_info = []
for table in tables:
  rows = table.find_all("ul", class_="list")
  for row in rows:
    country_links = row.find_all("a")
    for link in country_links:
      country_name = link.get_text(strip=True)
      country_url = base_url + link["href"]
      country_info.append({"Country": country_name, "URL": country_url})

# Compile data
data = []
for country in country_info:
  country_name = country["Country"]
  country_url = country["URL"]
  country_details = scrape_country_detail(country_url)
  # Append data for each relevant section and detail
  for section, details in country_details.items():
    for detail in details:
      data.append({"Country": country_name, "Section": section, "Detail": detail})

# Convert data to DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv("country_etiquette_data.csv", index=False)
