import os
from bs4 import BeautifulSoup

def extract_hrefs_from_folder(country_name: str, city_name: str):
    folder_path = os.path.join("data", country_name, city_name)
    hrefs = []

    # List all files in the directory
    for filename in os.listdir(folder_path):
        if filename.startswith(city_name) and filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            # Extract page number from filename
            try:
                page_num = filename.split("_")[-1].split(".")[0]  # e.g., "seattle_0_49.txt" -> "49"
            except Exception as e:
                print(f"Error extracting page number from {filename}: {e}")
                continue

            # Read and parse txt
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'lxml')
                
                # Find all <a> tags with href attributes
                for a_tag in soup.find_all('a', href=True):
                    href_with_page = f"{a_tag['href']}####page={page_num}####"
                    hrefs.append(href_with_page)

    return hrefs


# Example usage


if __name__ == "__main__":
    country = "wa"
    city = "seattle"
    urls = extract_hrefs_from_folder(country, city)
    
    print("this is the length of arrays:")
    print(+len(urls))
    for url in urls:
        print(url)
