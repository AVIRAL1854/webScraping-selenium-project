import pandas as pd

def export_to_csv_with_pandas(data: dict, output_file='event_data.csv'):
    rows = []

    for event_link, details in data.items():
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

    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False,encoding='utf-8-sig')



# testing function

# mock_data = {'https://www.eventbrite.com/e/seattle-breakfast-with-giraffes-a-film-by-soroush-sehat-tickets-1315622495299?aff=ebdssbdestsearch': {'organizer': 'Daricheh Cinema - USA', 'social_links': ['https://www.facebook.com/darichehcinema', 'https://www.twitter.com/darichehcinema'], 'banner_link': 'https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F937087553%2F4650103453%2F1%2Foriginal.20250116-044548?crop=focalpoint&fit=crop&w=600&auto=format%2Ccompress&q=75&sharp=10&fp-x=0.498106060606&fp-y=0.484&s=4695a85097dbd28b856083ba502a9eba', 'logo_url': 'https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F17089234%2F4650103453%2F2%2Foriginal.jpg?w=225&auto=format%2Ccompress&q=75&sharp=10&s=d4c363efd2658fa1b2d29c12a21c7a13', 'dateTime': 'Wednesday, April 23 · 7 - 9:30pm PDT', 'eventTitle': 'Seattle - Breakfast With Giraffes a film by Soroush Sehat'}, 'https://www.eventbrite.com/e/2025-aia-seattle-parti-tickets-1247608152569?aff=ebdssbdestsearch': {'organizer': 'AIA Seattle', 'social_links': ['https://www.facebook.com/AIASeattle', 'https://www.twitter.com/AIASeattle'], 'banner_link': 'https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F959507833%2F207163566514%2F1%2Foriginal.20250212-224617?crop=focalpoint&fit=crop&w=600&auto=format%2Ccompress&q=75&sharp=10&fp-x=0.5&fp-y=0.5&s=aae026494d388d8f770b8afbd7f0b0ce', 'logo_url': None, 'dateTime': 'Tuesday, April 22 · 6 - 8:30pm PDT', 'eventTitle': '2025 AIA Seattle Parti'}, 'https://www.eventbrite.com/e/an-evening-with-eckhart-tolle-in-seattle-tickets-1219229561439?aff=ebdssbdestsearch&keep_tld=1': {'organizer': 'Genius Productions', 'social_links': [], 'banner_link': 'https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F942761313%2F162678786657%2F1%2Foriginal.20250123-110019?w=600&auto=format%2Ccompress&q=75&sharp=10&rect=0%2C0%2C1020%2C510&s=8d7a444903f287ada7c553496d32f623', 'logo_url': 'https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F34503702%2F162678786657%2F2%2Foriginal.jpg?w=225&auto=format%2Ccompress&q=75&sharp=10&s=fad1cf01d2629e823ec3d4062598eb0d', 'dateTime': 'Saturday, May 10 · 7 - 9pm PDT. Doors at 6pm', 'eventTitle': 'An Evening with Eckhart Tolle in Seattle'}}

# export_to_csv_with_pandas(mock_data,"mock_data_checker.csv")

