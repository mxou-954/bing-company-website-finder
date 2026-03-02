import time
import urllib.parse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from config import BAD_PATTERNS, MAX_RESULTS, SEL_SELECTOR


def _is_valid_url(url: str) -> bool:
    lower = url.lower()
    return not any(bad in lower for bad in BAD_PATTERNS)


def search_official_site(driver: webdriver.Chrome, company_name: str) -> str:
    query = urllib.parse.quote_plus(company_name)
    url = f"https://www.bing.com/search?q={query}"

    try:
        driver.get(url)
    except TimeoutException:
        return ""

    time.sleep(1)

    links = driver.find_elements("css selector", SEL_SELECTOR)[:MAX_RESULTS]

    for elem in links:
        href = elem.get_attribute("href")
        if href and _is_valid_url(href):
            return href

    return ""