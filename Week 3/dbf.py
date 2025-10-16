from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def scrape_java_version_history(url: str, output_csv: str):
    """
    Scrapes the Java version history table from a given Wikipedia page using Selenium
    and saves the extracted data as a CSV file in the same folder.

    Parameters
    ----------
    url : str
        The URL of the Wikipedia page containing the Java version history table.
    output_csv : str
        The name of the CSV file to save the scraped data.

    Returns
    -------
    None
        Creates a CSV file in the same folder as the script containing the scraped table data.
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(2)
#extraction starts here
    table = driver.find_element(By.CSS_SELECTOR, "table.wikitable")
    headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]

    rows = []
    for tr in table.find_elements(By.TAG_NAME, "tr")[1:]:
        cells = tr.find_elements(By.TAG_NAME, "td")
        row = [cell.text.strip().replace("\n", " ") for cell in cells]
        if row:
            rows.append(row)

    df = pd.DataFrame(rows, columns=headers[:len(rows[0])])
    df.to_csv(output_csv, index=False, encoding="utf-8")

    driver.quit()
    print(f"✅ Scraping complete! Data saved as '{output_csv}' in the same folder.")


if __name__ == "__main__":
    scrape_java_version_history(
        url="https://www.dbf2002.com/news.html",
        output_csv="dbf.csv"
    )