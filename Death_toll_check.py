import pandas as pd
import re

# Load the Excel file
file_path = 'D:/Learn/Tableau/covid/Chronological Table of Epidemic and Pandemic Events in human History.xlsx'  # Update with your file path
df = pd.read_excel(file_path)

# Function to process the death toll estimates
def process_death_toll(death_toll):
    # Convert to string to handle different formats consistently
    death_toll = str(death_toll).strip()
    
    # Clean the input by removing any extra text and normalizing spaces
    death_toll_cleaned = re.sub(r'\s*\(.*?\)', '', death_toll).strip()  # Remove anything in parentheses
    death_toll_cleaned = re.sub(r'\s+', ' ', death_toll_cleaned)  # Normalize spaces
    
    print(f"Processing: '{death_toll_cleaned}'")  # Debug: Show what is being processed

    # Check if the cleaned input is a whole number
    if death_toll_cleaned.isdigit():
        return int(death_toll_cleaned)

    # Handle million or billion notation
    for unit in ['million', 'billion']:
        if unit in death_toll_cleaned:
            # Split on hyphen if present
            if '-' in death_toll_cleaned:
                parts = death_toll_cleaned.split('-')
                upper_limit = parts[1].strip().replace(',', '').replace(unit, '').strip()
                return int(float(upper_limit) * (1_000_000 if unit == 'million' else 1_000_000_000))
            else:
                number = death_toll_cleaned.replace(',', '').replace(unit, '').strip()
                return int(float(number) * (1_000_000 if unit == 'million' else 1_000_000_000))

    # Handle ranges like "5-10" or "25,000+"
    if "-" in death_toll_cleaned:
        parts = death_toll_cleaned.split("-")
        # Extract the upper limit
        upper_limit = parts[1].strip().replace(',', '').replace('+', '').strip()
        return int(upper_limit)  # Return the upper limit directly
    
    # Handle cases with "+" like "10,000+"
    if "+" in death_toll_cleaned:
        cleaned_number = death_toll_cleaned.replace('+', '').replace(',', '').strip()
        print(f"Trying to convert: '{cleaned_number}'")  # Debug: Show what is being converted
        return int(cleaned_number)
    
    # Handle cases with invalid characters or unexpected formats
    cleaned_number = re.sub(r'[^\d.]+', '', death_toll_cleaned)  # Remove all non-numeric characters except for '.'

    print(f"Cleaned number: '{cleaned_number}'")  # Debug: Show cleaned number

    if cleaned_number:
        try:
            return int(float(cleaned_number))  # Try to convert the cleaned number
        except ValueError:
            print(f"Failed to convert: '{cleaned_number}'")  # Debug: Show failed conversion
            pass  # Ignore and continue to prompt for input if conversion fails
    
    # If none of the conditions are met, ask for user input
    user_input = input(f"Encountered a new format: '{death_toll_cleaned}'. Please provide the upper limit value (or type 'Unknown'): ")
    
    # Allow 'Unknown' as a valid response
    if user_input.strip().lower() == "unknown":
        return "Unknown"  # Return 'Unknown' if user inputs 'Unknown'
    
    return int(user_input.strip())  # Convert user input to an integer

# Apply the processing function to the Death toll column (assumed to be in Column F)
df['G'] = df['Death toll (estimate)'].apply(process_death_toll)  # Save results in column G

# Display the DataFrame
print(df)

# Save the results back to an Excel file if desired
output_path = 'processed_death_toll.xlsx'
df.to_excel(output_path, index=False)
