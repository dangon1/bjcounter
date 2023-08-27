import csv
# To be used when want to round what spreadsheet sends to replace file content
def round_csv(input_filename, output_filename, decimal_places):
    with open(input_filename, newline='') as input_file, open(output_filename, 'w', newline='') as output_file:
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames

        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            for field in fieldnames:
                try:
                    row[field] = round(float(row[field]), decimal_places)
                except ValueError:
                    pass  # Ignore non-float fields

            writer.writerow(row)
