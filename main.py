from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
from extracting_organizerURL import extract_hrefs_from_folder
from extractingEachOrganizerDetails import extract_social_links_from_urls
from selenium.webdriver.firefox.options import Options
from uniqueURL import get_unique_urls
from exportToCsv import export_to_csv_with_pandas
import sys



# Firefox headless Options 

fireFox_options = Options()
fireFox_options.add_argument("--headless")
driver=webdriver.Firefox(options=fireFox_options)

queryCountry = sys.argv[1] if len(sys.argv) > 1 else ""
queryCity = sys.argv[2] if len(sys.argv) > 2 else ""

file=0


driver.get(f"https://www.eventbrite.com/d/{queryCountry}--{queryCity}/all-events/?page={1}")


# getting the total number of pages
try:
    pagination_elem = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="pagination-parent"]')
    pagination_text = pagination_elem.text 
    
    total_pages = int(pagination_text.split('of')[-1].strip())
    print("Total pages:", total_pages)
except Exception as e:
    print("Error extracting total pages:", e)


# getting events from the event list and saving it in data/country/city
for i in range(1,total_pages+1):

    print(f"Running page number :{i}/{total_pages}\n\n")
    driver.get(f"https://www.eventbrite.com/d/{queryCountry}--{queryCity}/all-events/?page={i}")


    elems=driver.find_elements(By.CLASS_NAME,"event-card-link ")


    # print(elems)
    print("yes this is started ....")

    print(f"{len(elems)} items found")

    output_dir = f"data/{queryCountry}/{queryCity}"
    os.makedirs(output_dir, exist_ok=True)


    for elem in elems:
        d=elem.get_attribute("outerHTML")
        with open(f"data/{queryCountry}/{queryCity}/{queryCity}_{file}.txt","w",encoding="utf-8") as f:
            f.write(d)
            file+=1
        

    print("completed")


driver.close()

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


