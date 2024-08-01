import csv

def read_csv_to_list_of_lists(file_path, start_line, end_line):
    """
    Reads a specified range of lines from a CSV file and returns the contents as a list of lists.

    Parameters:
    file_path (str): The path to the CSV file.
    start_line (int): The starting line number (1-based) to read from.
    end_line (int): The ending line number (inclusive, 1-based) to read until.

    Returns:
    list: A list of lists where each inner list represents a row from the specified range in the CSV file.
    """
    data = []

    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)

            # Skip lines before the start_line
            for _ in range(start_line - 1):
                next(reader, None)

            # Read lines from start_line to end_line
            for line_number, row in enumerate(reader, start=start_line):
                if line_number > end_line:
                    break
                data.append(row)

    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

    return data

# Example usage
file_path = 'example.csv'  # Replace with the path to your CSV file
start_line = 2  # Replace with the starting line number (1-based)
end_line = 4    # Replace with the ending line number (inclusive, 1-based)
data = read_csv_to_list_of_lists(file_path, start_line, end_line)

# Print the data
for row in data:
    print(row)
