import os
import re
import pandas as pd
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all_tables_from_website(url: str):
    """
    Scrapes all meaningful HTML tables from a webpage using Selenium
    and saves each as a CSV file inside an 'output' folder.

    Parameters
    ----------
    url : str
        The URL of the webpage containing tables.

    Returns
    -------
    None
        Creates one or more CSV files inside the 'output' folder.
    """

    # --- Create 'output' folder if it doesn't exist ---
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # --- Generate base filename from URL ---
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "")
    page_name = parsed_url.path.split("/")[-1] or "index"
    safe_page_name = re.sub(r'[^a-zA-Z0-9_-]', '_', page_name)
    base_name = f"{domain}_{safe_page_name}"

    # --- Setup Chrome (headless mode) ---
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print(f"🌐 Accessing: {url}")
        driver.get(url)

        # Wait until tables appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        tables = driver.find_elements(By.TAG_NAME, "table")
        print(f"🔍 Found {len(tables)} tables on the page.")

        valid_table_count = 0

        for idx, table in enumerate(tables, start=1):
            headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
            rows = []

            for tr in table.find_elements(By.TAG_NAME, "tr")[1:]:
                cells = tr.find_elements(By.TAG_NAME, "td")
                row = [cell.text.strip().replace("\n", " ") for cell in cells]
                if row:
                    rows.append(row)

            # Skip tiny/empty/infobox tables
            if len(rows) < 2 or (len(rows[0]) < 2 and len(headers) < 2):
                continue

            valid_table_count += 1

            # Normalize table structure
            max_columns = max(len(r) for r in rows)
            headers = headers[:max_columns] or [f"Column_{i+1}" for i in range(max_columns)]
            for row in rows:
                while len(row) < max_columns:
                    row.append("")

            df = pd.DataFrame(rows, columns=headers)
            output_csv = os.path.join(output_folder, f"{base_name}_table{valid_table_count}.csv")
            df.to_csv(output_csv, index=False, encoding="utf-8")

            print(f"✅ Saved: {output_csv} ({len(rows)} rows)")

        if valid_table_count == 0:
            print("⚠️ No suitable tables found (only layout/infobox tables detected).")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    finally:
        driver.quit()
        print("🧹 Browser closed.")


if __name__ == "__main__":
    scrape_all_tables_from_website("https://en.wikipedia.org/wiki/Oracle_Linux")
