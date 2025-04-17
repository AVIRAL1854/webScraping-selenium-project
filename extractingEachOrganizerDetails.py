from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from exportToCsv import export_to_csv_with_pandas
import os
from remove_duplicate_organizers import remove_duplicate_organizers

def extract_social_links_from_urls(urls ,queryCountry='default',queryCity='default'):
    # Setup headless Firefox
    fireFox_options = Options()
    fireFox_options.add_argument("--headless")  # Run in headless mode

    driver = webdriver.Firefox(options=fireFox_options)

    results = {}

    for url in urls:
        try:
            driver.get(url)
            time.sleep(1)  # Let page load
            # print(results)
            # Extract social links
            try:
                social_links_div = driver.find_element(By.CSS_SELECTOR, 'div.css-ojn45[data-testid="socialLinks"]')
                a_tags = social_links_div.find_elements(By.TAG_NAME, 'a')
                links = [a.get_attribute('href') for a in a_tags if a.get_attribute('href')]
            except NoSuchElementException:
                links = []

            # Extract organizer name
            try:
                organizer_element = driver.find_element(By.CLASS_NAME, 'descriptive-organizer-info-mobile__name-link')
                organizer_name = organizer_element.text.strip()
            except NoSuchElementException:
                organizer_name = "Organizer name not found"

            print(f"\n🔗 URL: {url}")
            print(f"👤 Organizer: {organizer_name}")
            print(f"📱 Social Links: {links}\n")

            results[url] = {
                "organizer": organizer_name,
                "social_links": links
            }

        except Exception as e:
            print(f"❌ Error processing {url}: {e}")
            results[url] = {
                "organizer": None,
                "social_links": []
            }

    driver.quit()


    output_dir = f"finalCSV/{queryCountry}/{queryCity}"
    os.makedirs(output_dir, exist_ok=True)
    # exporting as csv
    export_to_csv_with_pandas(results, f"{output_dir}/inputTestData.csv")

    # Now clean it by removing duplicate organizerName rows
    input_file = f"{output_dir}/inputTestData.csv"
    output_file = f"{output_dir}/uniqueTestData.csv"
    remove_duplicate_organizers(input_file, output_file)
    return results



# Uncomment to test with the list
# results = extract_social_links_and_organizer_from_urls(testUrl)
# print(results)




# testUrl =[
#     "https://www.eventbrite.com/e/seattle-breakfast-with-giraffes-a-film-by-soroush-sehat-tickets-1315622495299?aff=ebdssbdestsearch",
#     "https://www.eventbrite.com/e/2025-aia-seattle-parti-tickets-1247608152569?aff=ebdssbdestsearch"
#     ]


# extract_social_links_from_urls(testUrl,"India2")
