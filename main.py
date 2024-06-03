import subprocess
import os
import datetime

def read_names_from_file(file_path):
    """Reads a list of names from the given file and returns them as a list."""
    with open(file_path, 'r') as file:
        names = file.read().splitlines()
    return names

def search_for_names(names):
    """Searches for each name in the entire file system from the root directory and writes the results to a timestamped file."""
    # Ensure the results directory exists
    if not os.path.exists('results'):
        os.makedirs('results')

    for name in names:
        search_command = f'find / -iname "*{name}*" 2>/dev/null'  # Corrected command

        try:
            result = subprocess.run(search_command, capture_output=True, text=True, shell=True)  # Update to take string command
            if result.stdout:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                output_file_path = os.path.join('results', f'{current_time}.txt')
                with open(output_file_path, 'a') as output_file:
                    output_file.write(f'Results for search term: {name}\n')
                    output_file.write(result.stdout)
                    output_file.write('\n' + '-' * 80 + '\n')

                # Print the file locations
                print(f'Results for search term "{name}":')
                print(result.stdout)
            else:
                print(f"No results found for '{name}'.")
        except Exception as e:
            print(f"An error occurred while searching for '{name}': {e}")

def main():
    names = read_names_from_file('searches.txt')
    search_for_names(names)

if __name__ == "__main__":
    main()