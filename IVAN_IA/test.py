import os
import time
import csv
from urllib.parse import urljoin

from scraperapi_sdk import ScraperAPIClient
from bs4 import BeautifulSoup

API_KEY = "1611c54740770f029143378f83a357d1"
if not API_KEY:
    raise ValueError("Please set the SCRAPERAPI_KEY environment variable.")
client = ScraperAPIClient(API_KEY)

BASE_URL = 'https://www.thomasnet.com'

PROFILE_FIELDS = [
    'Company Name', 'Logo URL', 'Phone Number', 'Business Description',
    'Address', 'Products Services', 'Website', 'Website 2', 'Primary Company Type',
    'Additional Activities', 'Key Personnel', 'Diverse / Small Bus. Status',
    'Quality Certifications', 'Registration', 'Annual Sales', 'No of Employees',
    'Year Founded', 'Emails'
]


def fetch(url):
    print(f"Fetching: {url}")
    response = client.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {url}: {response.status_code}")
    time.sleep(1)  # polite delay
    return response.text


def get_category_links():
    html = fetch(BASE_URL)
    soup = BeautifulSoup(html, 'html.parser')
    cat_links = []
    for ul in soup.select('ul.sf-menu > li > a'):
        href = ul.get('href')
        if href and href.startswith('/browse'):
            cat_links.append(urljoin(BASE_URL, href))
    return list(set(cat_links))


def get_company_links(category_url):
    html = fetch(category_url)
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for tag in soup.select('div.mt-Card--company a.hit-title'):
        href = tag.get('href')
        if href and href.startswith('/company-'):
            links.append(urljoin(BASE_URL, href))
    return list(set(links))


def parse_company_profile(profile_url):
    html = fetch(profile_url)
    soup = BeautifulSoup(html, 'html.parser')
    data = {field: '' for field in PROFILE_FIELDS}

    name_tag = soup.find('h1', {'class': 'headline'})
    data['Company Name'] = name_tag.get_text(strip=True) if name_tag else ''

    logo_tag = soup.find('img', {'class': 'company-logo'})
    data['Logo URL'] = logo_tag['src'] if logo_tag and logo_tag.get('src') else ''

    for row in soup.select('div.company-info tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            key = cols[0].get_text(strip=True).rstrip(':')
            val = cols[1].get_text(strip=True)
            if key in data:
                data[key] = val

    email_tags = soup.select('a[href^="mailto:"]')
    emails = [a.get('href').replace('mailto:', '') for a in email_tags]
    data['Emails'] = ', '.join(emails)

    return data


def scrape_thomasnet(output_csv='thomasnet_companies.csv'):
    categories = get_category_links()
    print(f"Found {len(categories)} categories.")

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Thomasnet Link', *PROFILE_FIELDS])
        writer.writeheader()

        for cat in categories:
            print(f"Processing category: {cat}")
            company_links = get_company_links(cat)
            print(f"  {len(company_links)} companies found.")

            for link in company_links:
                try:
                    details = parse_company_profile(link)
                    row = {'Thomasnet Link': link, **details}
                    writer.writerow(row)
                except Exception as e:
                    print(f"Error parsing {link}: {e}")

    print(f"Scraping complete. Output saved to {output_csv}")

if __name__ == '__main__':
    scrape_thomasnet()
