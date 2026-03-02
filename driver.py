from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from config import DRIVER_PATH, PAGE_LOAD_TIMEOUT


def init_driver(driver_path: Optional[str] = None) -> webdriver.Chrome:
    path = driver_path or DRIVER_PATH

    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--log-level=3")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])

    if path:
        service = Service(path)
        driver = webdriver.Chrome(service=service, options=opts)
    else:
        driver = webdriver.Chrome(options=opts)

    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver