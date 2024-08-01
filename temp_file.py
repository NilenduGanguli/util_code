import tempfile
import csv
import os

def create_temp_csv(directory, data):
    # Create a temporary file with a .csv extension in the specified directory
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', dir=directory, mode='w', newline='') as temp_csv:
        writer = csv.writer(temp_csv)
        # Write data to the CSV file
        writer.writerows(data)
        # Get the temporary file's name
        temp_csv_name = temp_csv.name

    return temp_csv_name

# Example usage
directory = "/path/to/specified/directory"  # Replace with the desired directory path
data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "New York"],
    ["Bob", 25, "San Francisco"],
    ["Charlie", 35, "Los Angeles"]
]

# Create the temporary CSV file
temp_csv_path = create_temp_csv(directory, data)

# Print the path of the created temporary CSV file
print(f"Temporary CSV file created at: {temp_csv_path}")

# Read and print the content of the temporary CSV file (optional)
with open(temp_csv_path, 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# Optionally, delete the temporary file if no longer needed
# os.remove(temp_csv_path)
