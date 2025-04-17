import pandas as pd

def export_to_csv_with_pandas(data: dict, output_file='event_data.csv'):
    rows = []

    for event_link, details in data.items():
        row = {
            "organizerName": details.get("organizer", ""),
            "facebook": "",
            "instagram": "",
            "twitter": "",
            "personal website": "",
            "LinkedIn": "",
            "Pinterest": "",
            "WeChat": "",
            "WhatsApp": "",
            "TikTok": "",
            "eventbrite event link": event_link
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
    df.to_csv(output_file, index=False)



# testing function

# mock_data = {
#     "https://eventbrite.com/e/event-1": {
#         "organizer_name": "Tech Conference 2025",
#         "social_links": [
#             "https://facebook.com/techconf",
#             "https://twitter.com/techconf",
#             "https://linkedin.com/company/techconf"
#         ]
#     },
#     "https://eventbrite.com/e/event-2": {
#         "organizer_name": "Art Expo Global",
#         "social_links": [
#             "https://instagram.com/artexpo",
#             "https://artexpoglobal.com",
#             "https://pinterest.com/artexpo"
#         ]
#     },
#     "https://eventbrite.com/e/event-3": {
#         "organizer_name": "Startup Summit",
#         "social_links": [
#             "https://whatsapp.com/join/startupsummit",
#             "https://wechat.com/startupsummit",
#             "https://tiktok.com/@startupsummit"
#         ]
#     },
#     "https://eventbrite.com/e/event-4": {
#         "organizer_name": "Mystery Meetup",
#         "social_links": [
#             "https://unknownlink.com/mystery",
#         ]
#     }
# }

# export_to_csv_with_pandas(mock_data,"mock_data_checker.csv")

