from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

MAX_RETRIES = 4

def validate_xpaths(url, html, xpaths, retry_callback):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    results = {}

    for field, xpath in xpaths.items():
        verified = False
        current_xpath = xpath
        error = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                driver.find_element(By.XPATH, current_xpath)
                verified = True
                break
            except Exception as e:
                error = str(e)
                new_xpath = retry_callback(
                    html, field, current_xpath, error
                )
                current_xpath = new_xpath[field]

        results[field] = {
            "xpath": current_xpath,
            "verified": verified,
            "attempts": attempt,
            "error": None if verified else error
        }

    driver.quit()
    return results
