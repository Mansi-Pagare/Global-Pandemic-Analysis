Country to continent chnage python script

import pandas as pd

# Load the historical data
historical_data = pd.read_excel('D:\Learn\Tableau\covid\processed_death_toll2.xlsx')

# Load the country-to-continent mapping
country_continent_mapping = pd.read_excel('D:\Learn\Tableau\covid\Cu2ctt.xlsx')

# Ensure the mapping file has the right structure
# Assume the mapping file has columns 'Country' and 'Continent'
country_continent_mapping.columns = ['Country', 'Continent']

# Create a function to determine continents based on locations from multiple columns
def get_continents(row):
    # Collect all location columns (assuming they are named Location_1, Location_2, ..., Location_7)
    locations = []
    for i in range(1, 8):
        location = row[f'Location_{i}']
        if pd.notnull(location):  # If the location is not NaN
            locations.append(location.strip())

    continents = set()  # Use a set to avoid duplicates

    # Check each location and map it to its continent
    for location in locations:
        if location in country_continent_mapping['Country'].values:
            continent = country_continent_mapping.loc[country_continent_mapping['Country'] == location, 'Continent'].values[0]
            continents.add(continent)

    return ', '.join(continents)  # Return as a comma-separated string

# Apply the function to each row to create a new 'Continents' column
historical_data['Continents'] = historical_data.apply(get_continents, axis=1)

# Split the 'Continents' column into separate columns for each continent (if desired)
continent_columns = historical_data['Continents'].str.get_dummies(sep=', ')
historical_data = pd.concat([historical_data, continent_columns], axis=1)

# Save the modified dataframe back to an Excel file
historical_data.to_excel('D:\Learn\Tableau\covid\processed_death_toll2.xlsx', index=False)
