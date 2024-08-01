import csv

def read_csv_to_list_of_lists(file_path):
    """
    Reads a CSV file and returns its contents as a list of lists.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    list: A list of lists where each inner list represents a row from the CSV file.
    """
    data = []

    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)

    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

    return data

# Example usage
file_path = 'example.csv'  # Replace with the path to your CSV file
data = read_csv_to_list_of_lists(file_path)

# Print the data
for row in data:
    print(row)
