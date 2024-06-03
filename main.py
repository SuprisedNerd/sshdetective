import subprocess
import os
import datetime

def read_names_from_file(file_path):
    """Reads a list of names from the given file and returns them as a list."""
    with open(file_path, 'r') as file:
        names = file.read().splitlines()
    return names

def search_for_names(names):
    """Searches for each name in the entire file system and prints the results."""
    search_terms = []
    for name in names:
        search_terms.extend(['-o', '-iname', f'"*{name}*"'])  # Use wildcard to match any occurrence of the name

    # Join the search terms with the '-o' (OR) operator
    search_command = ['find', '.', '('] + search_terms + [')', '2>/dev/null']

    try:
        result = subprocess.run(search_command, capture_output=True, text=True)
        if result.stdout:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            with open(f"results/{current_time}.txt", 'w') as output_file:
                output_file.write(result.stdout)
        else:
            print("No results found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    names = read_names_from_file('searches.txt')
    search_for_names(names)

if __name__ == "__main__":
    main()