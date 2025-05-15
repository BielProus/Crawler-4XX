import csv
import time
import requests
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

visited = set()
errors = []

def is_same_domain(base_url, target_url):
    return urlparse(base_url).netloc == urlparse(target_url).netloc

def get_all_links(driver, base_url):
    links = set()
    try:
        elements = driver.find_elements(By.TAG_NAME, 'a')
        for elem in elements:
            href = elem.get_attribute('href')
            if href and is_same_domain(base_url, href):
                links.add(href.split('#')[0])
    except Exception as e:
        print(f"Error obtenint enllaços: {e}")
    return links

def check_url_status(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        if response.status_code >= 400 and response.status_code < 500:
            return response.status_code
    except requests.RequestException:
        return 499
    return None

def crawl(driver, base_url, current_url):
    if current_url in visited:
        return
    visited.add(current_url)

    driver.get(current_url)
    time.sleep(1)

    links = get_all_links(driver, base_url)

    for link in links:
        status = check_url_status(link)
        if status:
            print(f"[ERROR {status}] {link} (origen: {current_url})")
            errors.append((link, status, current_url))
        crawl(driver, base_url, link)

def generate_csv_report(filename='errors_4xx.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL amb error', 'Codi HTTP', 'Pàgina d\'origen'])
        writer.writerows(errors)

if __name__ == '__main__':
    start_url = 'https://httpstat.us/'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-background-networking')
    chrome_options.add_argument('--disable-sync')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-default-apps')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-first-run')
    chrome_options.add_argument('--no-default-browser-check')
    chrome_options.add_argument('--disable-client-side-phishing-detection')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        crawl(driver, start_url, start_url)
    finally:
        driver.quit()

    generate_csv_report()

