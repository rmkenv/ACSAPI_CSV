
# Commented out IPython magic to ensure Python compatibility.
# %pip install census

import csv
from census import Census
from tabulate import tabulate

api_key = "xyz123"  # Replace with your actual API key
census_client = Census(api_key)

# Create an empty list to store the data
census_data_list = []

csv_file_path = "/content/fcoi.csv"  # Replace with the actual path to your CSV file

# Open the CSV file
with open(csv_file_path, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        state = row["STATEFIPS"]
        county = row["COUNTYFIPS"]
        tract = row["TRACT"]
        latitude = row["latitude"]  # Replace with the correct column name for latitude
        longitude = row["longitude"]  # Replace with the correct column name for longitude

        # Perform index match using the Census API
        # Make a request to the API to get the relevant data
        census_data = census_client.acs5.state_county_tract(
            ("NAME","B01003_001E", "B01001_002E", "B01001_026E", "B01001B_001E", "B01001I_001E", "B06012_004E"),  # Specify the desired variables
            state,
            county,
            tract,
            year=2020,  # Replace with the desired census year
            lat=latitude,  # Include latitude in the API request
            lon=longitude  # Include longitude in the API request
        )

        # Process the census data returned by the API
        for result in census_data:
            name = result["NAME"]
            total_population = result["B01003_001E"]
            male_population = result["B01001_002E"]
            female_population = result["B01001_026E"]
            black = result["B01001B_001E"]
            latino = result["B01001I_001E"]
            poverty = result["B06012_004E"]

            # Create a dictionary to store the census data for each row
            census_row = {
                "name": name,
                "total_population": total_population,
                "male_population": male_population,
                "female_population": female_population,
                "black": black,
                "latino": latino,
                "poverty": poverty,
                 "latitude": latitude,  # Include latitude in the census data
                "longitude": longitude  # Include longitude in the census
            }
            # Append the census row to the list
            census_data_list.append(census_row)

# Convert the census data list into a table
table = []
for row in census_data_list:
    table.append([[key.replace('_', ' ').capitalize(), str(value)] for key, value in row.items()])
formatted_table = tabulate(table, headers=["Field", "Value"], tablefmt="pipe")

# Print the formatted table
print(formatted_table)

csv_output_path = "/content/output.csv"  # Replace with path

csv_output_path = "/content/output.csv"  # Replace with the desired output file path

# Write the census data to the CSV file
with open(csv_output_path, "w", newline="") as csv_file:
    fieldnames = census_data_list[0].keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write each row of census data
    for row in census_data_list:
        writer.writerow(row)

print("CSV file saved successfully!")
