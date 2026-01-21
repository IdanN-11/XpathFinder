import json
import re  # ← Add this!
from grok_client import ask_grok
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def generate_xpaths(html_doc="", prompt="", extra_context="", test_url=None):
    """
    Generates XPaths using Grok and validates them with Selenium.
    If test_url is provided, Selenium loads the URL instead of html_doc.
    """

    # 1️⃣ Ask Grok for XPaths
    raw_fields = ask_grok(html_doc, prompt, extra_context)

    # 2️⃣ Validate Grok response
    validated_fields = {}
    xpath_pattern = re.compile(r"^\/{1,2}.*")

    for field, xpath in raw_fields.items():
        if isinstance(xpath, str) and xpath_pattern.match(xpath.strip()):
            validated_fields[field] = xpath.strip()
        else:
            print(f"⚠️ Skipping invalid XPath from Grok for field '{field}': {xpath}")

    # 3️⃣ Selenium setup
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    import tempfile, os

    options = Options()
    options.add_argument("--headless=new")
    driver_path = Service()  # assumes chromedriver in PATH
    driver = webdriver.Chrome(service=driver_path, options=options)

    # 4️⃣ Load page in Selenium
    if test_url:
        driver.get(test_url)
    else:
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8")
        tmp_file.write(html_doc)
        tmp_file.close()
        file_url = f"file:///{tmp_file.name.replace(os.sep, '/')}"
        driver.get(file_url)

    # 5️⃣ Verify XPaths
    final_fields = {}
    for field, xpath in validated_fields.items():
        try:
            driver.find_element(By.XPATH, xpath)
            final_fields[field] = xpath
        except Exception:
            print(f"⚠️ Selenium could NOT find element for XPath '{xpath}' (field '{field}')")

    driver.quit()

    if not test_url:
        os.unlink(tmp_file.name)

    return final_fields
