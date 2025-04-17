import csv

def remove_duplicate_organizers(input_file, output_file):
    seen = set()
    unique_rows = []

    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # read the header
        unique_rows.append(headers)

        for row in reader:
            organizer = row[0].strip()
            if organizer not in seen:
                seen.add(organizer)
                unique_rows.append(row)

    # Write the unique rows to a new file
    with open(output_file, 'w', newline='', encoding='utf-8') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerows(unique_rows)

    print(f"Removed duplicates. Unique entries written to '{output_file}'.")

