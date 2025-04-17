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
            time.sleep(2)  # Let page load
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






            # extracting logo url
            try:
  
                svg = driver.find_element(By.CSS_SELECTOR, 'svg[data-spec="spec-avatar"]')
                image_tag = svg.find_element(By.TAG_NAME, "image")
                logoUrl = image_tag.get_attribute("href") or image_tag.get_attribute("xlink:href")
                # print("Logo URL:", logoUrl)

            except NoSuchElementException:
                print("Error: logo image not found.")
                logoUrl = None






            # extracting banner url 
            try:
                # Locate the image using data-testid attribute
                img = driver.find_element(By.CSS_SELECTOR, '[data-testid="hero-img"]')
                bannerSrc = img.get_attribute("src")
                

            except NoSuchElementException:
                print( "Error: Image with data-testid='hero-img' not found.")
                bannerSrc=None
            #extracting date and time 
            try:
                datetime_span = driver.find_element(By.CLASS_NAME, "date-info__full-datetime")
                datetime_text = datetime_span.text.strip()
            except NoSuchElementException:
                print( "Error: date and time not found")
                datetime_text="N/A"
            
            #extracting event title
            try:
                title_element = driver.find_element(By.CLASS_NAME, "event-title")
                eventTitle = title_element.text.strip()


            except NoSuchElementException:
                print( "Error: event title not found")
                eventTitle="N/A"




            print(f"\n🔗 URL: {url}")
            print(f"👤 Organizer: {organizer_name}")
            print(f"📱 Social Links: {links}\n")
            print(f" 🔗 banner Url:{bannerSrc}\n")
            print(f" 🔗 logo URL:{logoUrl}\n")
            print(f" 👤 date and time:{datetime_text}\n")
            print(f" 📱 eventTitle:{eventTitle}\n")
            results[url] = {
                "organizer": organizer_name,
                "social_links": links,
                "banner_link":bannerSrc,
                "logo_url":logoUrl,
                "dateTime":datetime_text,
                "eventTitle":eventTitle

            }
        except Exception as e:
            print(f"❌ Error processing {url}: {e}")
            results[url] = {
                "organizer": None,
                "social_links": [],
                 "banner_link":None,
                "logo_url":None,
                "dateTime":None,
                "eventTitle":None
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
#     "https://www.eventbrite.com/e/2025-aia-seattle-parti-tickets-1247608152569?aff=ebdssbdestsearch",
#     "https://www.eventbrite.com/e/an-evening-with-eckhart-tolle-in-seattle-tickets-1219229561439?aff=ebdssbdestsearch&keep_tld=1",
#     "https://www.eventbrite.com/e/how-to-holistically-heal-your-trauma-a-shadow-work-workshop-seattle-wa-tickets-1315458986239?aff=erellivmlt&_gl=1*6ftbws*_up*MQ..*_ga*MTg5MjE3ODQ0OC4xNzQ0OTE5OTIz*_ga_TQVES5V6SH*MTc0NDkxOTkyMi4xLjEuMTc0NDkyMTMwNi4wLjAuMA..*_ga_D6TD2GD2ER*MTc0NDkyMTMxMC4xLjAuMTc0NDkyMTMxMC4wLjAuMA.."
#     ]


# extract_social_links_from_urls(testUrl,"India2")
