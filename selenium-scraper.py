from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import time
import utils


# Path to the chromedriver.exe
PATH = "C:\Program Files\chromedriver.exe"

options = webdriver.ChromeOptions()

options.add_experimental_option("prefs", {
  "download.default_directory": r"C:\Users\xxx\Downloads",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

driver = webdriver.Chrome(PATH, chrome_options=options)

url = 'https://website.com/'

driver.get(url)
print(driver.title)

# Select object for the dropdown menu
cpt_group = Select(driver.find_element_by_id("ddlGroup"))
plan_group = Select(driver.find_element_by_id("ddlLOB"))

# Capture all options in the dropdown
cpt_options = cpt_group.options
plan_options = plan_group.options

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

for i in range(1, len(cpt_options)):

    cpt_group = Select(driver.find_element_by_id("ddlGroup"))

    # Capture all options in the dropdown
    cpt_options = cpt_group.options

    cpt_option = cpt_options[i]
    # plan_option = 'ABH of Michigan'


    print(f"Trying {cpt_option.text}")
    cpt_group.select_by_visible_text(cpt_option.text)

    plan_group = Select(driver.find_element_by_id("ddlLOB"))
    plan_options = plan_group.options
    plan_option = plan_options[1]
    print(f"Trying {plan_option.text}")
    plan_group.select_by_value(plan_option.text)

    print(f"Trying Search")

    search_element = driver.find_element_by_id("btnSearch")

    print("Selecting PA required")
    pa_element = driver.find_element_by_id("chkPAReqd")
    pa_element.click()

    print("Trying Search click")
    # time.sleep(5)
    search_element.click()
    time.sleep(5)

    # Waiting for the export to be ready
    try:
        print("Trying Export")
        export_element = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.ID, "btnExport"))
        )
        print("Trying Export click")
        export_element.click()
        driver.get(url)

    except:
        print("Error exporting")

filestore = r"C:\Users\xxx\Downloads\filestore"
utils.parse_html_to_db(filestore)
