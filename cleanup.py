import os

def delete_all_files_in_directory(directory):
    """
    Deletes all files in the specified directory.

    Parameters:
    directory (str): The path to the directory where files will be deleted.

    Returns:
    None
    """
    if not os.path.isdir(directory):
        print(f"The specified path '{directory}' is not a directory or does not exist.")
        return

    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):  # Check if it's a file
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            else:
                print(f"Skipped non-file: {file_path}")

    except Exception as e:
        print(f"An error occurred while deleting files: {e}")

# Example usage
directory = "/path/to/specified/directory"  # Replace with the desired directory path
delete_all_files_in_directory(directory)
