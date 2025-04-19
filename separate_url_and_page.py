def separate_url_and_page(modified_href: str):
    try:
        if '####page=' in modified_href:
            url_part, page_part = modified_href.split('####page=')
            page_number = int(page_part.replace('####', ''))
            return url_part, page_number
        else:
            return modified_href, None
    except Exception as e:
        print(f"Error processing URL: {modified_href} - {e}")
        return modified_href, None
