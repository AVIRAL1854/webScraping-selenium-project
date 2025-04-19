from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from exportToCsv import export_to_csv_with_pandas
import os
import json
from remove_duplicate_organizers import remove_duplicate_organizers
import pandas as pd
from separate_url_and_page import separate_url_and_page

def extract_social_links_from_urls(urls, queryCountry='default', queryCity='default'):
    # Setup headless Firefox
    fireFox_options = Options()
    fireFox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=fireFox_options)

    results = {}

    # Progress report paths
    progress_report_dir = f"progressReport/{queryCountry}/{queryCity}"
    os.makedirs(progress_report_dir, exist_ok=True)
    progress_report_path = os.path.join(progress_report_dir, "progress_report.json")

    # Load or initialize progress report
    if os.path.exists(progress_report_path):
        with open(progress_report_path, "r") as f:
            progress_report = json.load(f)
    else:
        progress_report = {
            "totalPages": 0,
            "totalPagesReal":0,
            "lastRunningPage": 0,
            "pageError": [],
            "urlArray": [],
            "lastURLCounter": 0,
            "urlError": [],
            "totalUrls": len(urls)
        }

    # Update totalUrls
    progress_report["totalUrls"] = len(urls)

    # Resume logic: skip already processed URLs
    start_index = progress_report.get("lastURLCounter", 0)
    urls_to_process = urls[start_index:]

    # print(f"Resuming scraping from URL index {start_index} out of {len(urls)}")


    try:
        for idx, original_url in enumerate(urls_to_process, start=start_index):
            start_index = progress_report.get("lastURLCounter", 0)
            print(f"\n\nResuming scraping from URL index {start_index} out of {len(urls)}\n\n")
            try:
                url, page_number = separate_url_and_page(original_url)
                driver.get(url)
                time.sleep(2)

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

                # Extract logo URL
                try:
                    svg = driver.find_element(By.CSS_SELECTOR, 'svg[data-spec="spec-avatar"]')
                    image_tag = svg.find_element(By.TAG_NAME, "image")
                    logoUrl = image_tag.get_attribute("href") or image_tag.get_attribute("xlink:href")
                except NoSuchElementException:
                    logoUrl = None

                # Extract banner URL
                try:
                    img = driver.find_element(By.CSS_SELECTOR, '[data-testid="hero-img"]')
                    bannerSrc = img.get_attribute("src")
                except NoSuchElementException:
                    bannerSrc = None

                # Extract date and time
                try:
                    datetime_span = driver.find_element(By.CLASS_NAME, "date-info__full-datetime")
                    datetime_text = datetime_span.text.strip()
                except NoSuchElementException:
                    datetime_text = "N/A"

                # Extract event title
                try:
                    title_element = driver.find_element(By.CLASS_NAME, "event-title")
                    eventTitle = title_element.text.strip()
                except NoSuchElementException:
                    eventTitle = "N/A"

                #extract number of followers organizer have

                try:
                    followers_element = driver.find_element(By.CLASS_NAME, "organizer-stats__highlight")
                    strong_tag = followers_element.find_element(By.TAG_NAME, "strong")
                    followers_count = strong_tag.text.strip()
                except NoSuchElementException:
                    followers_count = None


                # Debug output
                print(f"\n🔗 URL: {url}")
                print(f"\n🔗 pageNumber: {page_number}")
                print(f"👤 Organizer: {organizer_name}")
                print(f"📱 Social Links: {links}")
                print(f"🔗 Banner URL: {bannerSrc}")
                print(f"🔗 Logo URL: {logoUrl}")
                print(f"📆 Date & Time: {datetime_text}")
                print(f"📝 Event Title: {eventTitle}\n")

                results[url] = {
                    "organizer": organizer_name,
                    "followersCount":followers_count,
                    "social_links": links,
                    "banner_link": bannerSrc,
                    "logo_url": logoUrl,
                    "dateTime": datetime_text,
                    "eventTitle": eventTitle,
                    "page_number": page_number 

                }

                # Update progress
                progress_report["urlArray"].append(url)
                progress_report["lastURLCounter"] = idx + 1
                # progress_report["urlError"] = ""

            except Exception as e:
                print(f"❌ Error processing {url}: {e}")
                results[url] = {
                    "organizer": None,
                    "followersCount":followers_count,
                    "social_links": [],
                    "banner_link": None,
                    "logo_url": None,
                    "dateTime": None,
                    "eventTitle": None,
                    "page_number": page_number 
                }
                progress_report["urlError"].append({
                "url": url,
                "error": str(e)
            })
                # break  # Optional: stop on error

            # Save progress after every URL
            with open(progress_report_path, "w") as f:
                json.dump(progress_report, f, indent=2)

    finally:
        driver.quit()

        # Prepare file paths
        output_dir = f"finalCSV/{queryCountry}/{queryCity}"
        os.makedirs(output_dir, exist_ok=True)

        input_file = f"{output_dir}/inputTestData.csv"

        if os.path.exists(input_file):
            # Load existing data
            existing_df = pd.read_csv(input_file)

            # Convert new results (dict) to DataFrame using same logic as export_to_csv_with_pandas
            rows = []
            for event_link, details in results.items():
                row = {
                    "organizerName": details.get("organizer", ""),
                    "followersCount":details.get("followers_count",""),
                    "eventTitle": details.get("eventTitle", ""),
                    "dateTime": details.get("dateTime", ""),
                    "banner_link": details.get("banner_link", ""),
                    "logo_url": details.get("logo_url", ""),
                    "facebook": "",
                    "instagram": "",
                    "twitter": "",
                    "personal website": "",
                    "LinkedIn": "",
                    "Pinterest": "",
                    "WeChat": "",
                    "WhatsApp": "",
                    "TikTok": "",
                    "eventbrite event link": event_link,
                    "page_number": details.get("page_number", "")
                }

                for link in details.get("social_links", []):
                    if "facebook.com" in link:
                        row["facebook"] = link
                    elif "instagram.com" in link:
                        row["instagram"] = link
                    elif "twitter.com" in link or "x.com" in link:
                        row["twitter"] = link
                    elif "linkedin.com" in link:
                        row["LinkedIn"] = link
                    elif "pinterest.com" in link:
                        row["Pinterest"] = link
                    elif "wechat.com" in link:
                        row["WeChat"] = link
                    elif "whatsapp.com" in link:
                        row["WhatsApp"] = link
                    elif "tiktok.com" in link:
                        row["TikTok"] = link
                    else:
                        row["personal website"] = link

                rows.append(row)

            new_df = pd.DataFrame(rows)

            # Append new data
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.to_csv(input_file, index=False, encoding='utf-8-sig')
        else:
            # First time writing, so just use your function
            export_to_csv_with_pandas(results, input_file)

        # Remove duplicates
        output_file = f"{output_dir}/uniqueTestData.csv"
        remove_duplicate_organizers(input_file, output_file)


        return results


# Uncomment to test with the list
# results = extract_social_links_and_organizer_from_urls(testUrl)
# print(results)




testUrl =[
    "https://www.eventbrite.com/e/seattle-new-friends-single-professionals-mixer-33-42-group-tickets-1305657720389?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/in-person-class-hand-rolled-sushi-seattle-tickets-1287920447729?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/bearracuda-seattles-locker-room-party-tickets-1317654312519?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/the-well-day-retreat-for-mothers-and-gestational-parents-tickets-1284798580139?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/sake-x-jazz-presents-trio-samambaia-when-spring-comes-at-kais-bistro-tickets-1309095964269?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/mediumship-demonstration-tickets-1287926415579?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/introduction-to-sensual-dance-and-low-flow-tickets-1079459706039?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/press-sip-a-luxury-press-on-nail-experience-tickets-1305085729549?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/km-huber-with-suzanne-morrison-call-of-the-owl-woman-tickets-1312123068419?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/4-day-pmp-examination-certification-training-course-in-bellevue-wa-tickets-975711448207?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/lucky-seven-casino-night-at-the-collective-seattle-tickets-1307392539279?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/agile-certification-from-pmi-in-seattle-tickets-1219123915449?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/the-rose-codes-unlock-your-intuition-creativity-higher-wisdom-tickets-1316663549119?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/jazzvox-house-concert-john-proulx-alyssa-allgood-seattle-madrona-2-tickets-1210223584319?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/suite-restaurant-lounge-bellevue-paint-your-pet-tickets-1258923557249?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/2025-world-tai-chi-and-quigong-day-free-tai-chi-seminar-tickets-1285182658929?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/in-person-cisa-exam-prep-course-in-seattle-tickets-1112313783469?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/elev8-tickets-1295202659019?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/seattle-shores-love-scavenger-hunt-for-couples-date-night-tickets-821477650767?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/healthcare-and-business-networking-elevating-your-potential-seattle-tickets-1268610902359?aff=ebdssbdestsearch",
    "https://www.eventbrite.com/e/sips-silent-reading-tickets-1307342750359?aff=ebdssbdestsearch"
    
    ]


extract_social_links_from_urls(testUrl,"Indiasdsd2","bhopalsdsdsdsd11")
