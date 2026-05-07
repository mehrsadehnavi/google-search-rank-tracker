from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_site_rankings(keyword, sites, max_pages=10):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    rankings = {site: None for site in sites}

    try:
        driver.get("https://www.google.com")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of(search_box)
        )
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        for page in range(max_pages):
            time.sleep(2)

            results = driver.find_elements(By.XPATH, "//div[@class='g']//a[@href]")

            for rank, result in enumerate(results, start=1):
                url = result.get_attribute("href")
                for site in sites:
                    if site in url and rankings[site] is None:
                        rankings[site] = page * 10 + rank
            try:
                next_button = driver.find_element(By.XPATH, "//a[@id='pnnext']")
                next_button.click()
            except:
                break

    finally:
        driver.quit()

    return rankings

if __name__ == "__main__":
    keyword = "selenium"
    sites = ["https://www.selenium.dev", "https://en.wikipedia.org"]
    rankings = get_site_rankings(keyword, sites)
    for site, rank in rankings.items():
        print(f"{site}: {rank if rank is not None else 'Not found in the first 10 pages'}")
