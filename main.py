from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import os
import sys

# Custom imports
from extracting_organizerURL import extract_hrefs_from_folder
from extractingEachOrganizerDetails import extract_social_links_from_urls
from uniqueURL import get_unique_urls
from exportToCsv import export_to_csv_with_pandas

# Initialize variables
queryCountry = sys.argv[1] if len(sys.argv) > 1 else "us"
queryCity = sys.argv[2] if len(sys.argv) > 2 else "new-york"
file = 0
total_pages = 1  # Default fallback

# Firefox headless options
fireFox_options = Options()
fireFox_options.add_argument("--headless")

try:
    driver = webdriver.Firefox(options=fireFox_options)
except Exception as e:
    print(f"Error initializing Firefox WebDriver: {e}")
    sys.exit(1)

# Try to open the first page
try:
    url = f"https://www.eventbrite.com/d/{queryCountry}--{queryCity}/all-events/?page=1"
    driver.get(url)
except Exception as e:
    print(f"Failed to load the initial URL: {e}")
    driver.quit()
    sys.exit(1)

# Get total number of pages
try:
    pagination_elem = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="pagination-parent"]')
    pagination_text = pagination_elem.text
    total_pages = int(pagination_text.split('of')[-1].strip())
    print("Total pages:", total_pages)
except Exception as e:
    print("Error extracting total pages, defaulting to 1:", e)

# Ensure output directory exists
output_dir = f"data/{queryCountry}/{queryCity}"
try:
    os.makedirs(output_dir, exist_ok=True)
except Exception as e:
    print(f"Error creating output directory '{output_dir}': {e}")
    driver.quit()
    sys.exit(1)

# Loop through event pages
for i in range(1, 3):
    try:
        print(f"Running page number: {i}/{total_pages}\n")
        driver.get(f"https://www.eventbrite.com/d/{queryCountry}--{queryCity}/all-events/?page={i}")
        time.sleep(3)  # Give time for page to load

        try:
            elems = driver.find_elements(By.CLASS_NAME, "event-card-link ")
            print("Started scraping...")
            print(f"{len(elems)} items found on page {i}")
        except Exception as e:
            print(f"Error finding event elements on page {i}: {e}")
            continue

        for elem in elems:
            try:
                d = elem.get_attribute("outerHTML")
                file_path = os.path.join(output_dir, f"{queryCity}_{file}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(d)
                file += 1
            except Exception as e:
                print(f"Failed to write data to file {file_path}: {e}")

        print(f"Page {i} completed\n")

    except Exception as e:
        print(f"Unexpected error while processing page {i}: {e}")

# Close the driver safely
try:
    driver.quit()
except Exception as e:
    print(f"Error while closing the WebDriver: {e}")


print(f"Now starting extracting links from data/{queryCountry}/{queryCity}/..\n\n\n")



try:
    RawUrls = extract_hrefs_from_folder(queryCountry, queryCity)
    urls=get_unique_urls(RawUrls)
except Exception as e:
    print(f"Error extracting Links or hrefs from  data/{queryCountry}/{queryCity}/.. \n\n\n:", e)



print(f"Successfully extracted links or hrefs from data/{queryCountry}/{queryCity}/..")


# Now extracting social media links for each organizer

social_links = extract_social_links_from_urls(urls,queryCountry,queryCity)

print("\n\n-----------------Phase 1 social link extracted Successfully ----------------\n\n")

for url, details in social_links.items():
    print(f"\nOrganizer URL: {url}")
    print(f"Organizer Name: {details.get('organizer', 'N/A')}")
    print("Social Links:")
    for link in details.get("social_links", []):
        print(link)

print("\n\nSuccessfully extracted social media links")


