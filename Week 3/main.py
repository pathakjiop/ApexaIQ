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


def scrape_table_from_website(url: str):
    """
    Scrapes the first HTML table found on a webpage using Selenium
    and saves it as a CSV file inside the 'output' folder, 
    with a name based on the website and page.

    Parameters
    ----------
    url : str
        The URL of the webpage containing the table.
    """

    # --- Create output folder ---
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # --- Generate output filename based on URL ---
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "")
    page_name = parsed_url.path.split("/")[-1] or "index"
    safe_page_name = re.sub(r'[^a-zA-Z0-9_-]', '_', page_name)
    output_csv = os.path.join(output_folder, f"{domain}_{safe_page_name}.csv")

    # --- Setup Chrome (headless mode) ---
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print(f"\n🌐 Accessing: {url}")
        driver.get(url)

        # Wait until at least one table appears
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        print("📋 Extracting table headers and rows...")
        headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
        rows = []

        for tr in table.find_elements(By.TAG_NAME, "tr")[1:]:
            cells = tr.find_elements(By.TAG_NAME, "td")
            row = [cell.text.strip().replace("\n", " ") for cell in cells]
            if row:
                rows.append(row)

        if not rows:
            raise ValueError("❌ No data rows found in the table.")

        # Normalize table
        max_columns = max(len(r) for r in rows)
        headers = headers[:max_columns] or [f"Column_{i+1}" for i in range(max_columns)]
        for row in rows:
            while len(row) < max_columns:
                row.append("")

        # Save as CSV inside /output/
        df = pd.DataFrame(rows, columns=headers)
        df.to_csv(output_csv, index=False, encoding="utf-8")

        print(f"✅ Scraping complete! Saved as: '{output_csv}'")

    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")

    finally:
        driver.quit()
        print("🧹 Browser closed.")


if __name__ == "__main__":
    urls = [
        "https://en.wikipedia.org/wiki/Java_version_history",
        "https://dotnet.microsoft.com/en-us/download/dotnet/8.0",
        "https://learn.microsoft.com/en-us/windows-server/get-started/windows-server-release-info",
        "https://en.wikipedia.org/wiki/Oracle_Linux",
        "https://en.wikipedia.org/wiki/SUSE_Linux_Enterprise",
        "https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information",
        "https://versionsof.net/core/8.0/8.0.0/",
    ]

    for link in urls:
        scrape_table_from_website(link)
