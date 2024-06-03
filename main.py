import subprocess
import os
import datetime

def read_names_from_file(file_path):
    """Reads a list of names from the given file and returns them as a list."""
    try:
        with open(file_path, 'r') as file:
            names = file.read().splitlines()
        return names
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred while reading from {file_path}: {e}")
        return []

def write_search_results(name, results, output_file_path):
    """Writes the search results to the output file."""
    with open(output_file_path, 'a') as output_file:
        output_file.write(f'Results for search term: {name}\n')
        output_file.write(results)
        output_file.write('\n' + '-' * 80 + '\n')

def search_for_names(names, output_file_path):
    """Searches for each name in the entire file system from the root directory and writes the results to the file."""
    # Ensure the results directory exists
    if not os.path.exists('results'):
        os.makedirs('results')

    for name in names:
        search_command = f'find / -iname "*{name}*" 2>/dev/null'  # Corrected command

        try:
            result = subprocess.run(search_command, capture_output=True, text=True, shell=True)  # Update to take string command
            if result.stdout:
                write_search_results(name, result.stdout, output_file_path)

                # Print the file locations
                print(f'Results for search term "{name}":')
                print(result.stdout)
            else:
                print(f"No results found for '{name}'.")
        except Exception as e:
            print(f"An error occurred while searching for '{name}': {e}")

def read_filters_and_search_contents(filter_file_path, results_file_path):
    """Reads the filter lines and searches the contents of the result files for matching lines."""
    try:
        with open(filter_file_path, 'r') as filter_file:
            filters = filter_file.read().splitlines()

        with open(results_file_path, 'r') as results_file:
            result_files = results_file.read().splitlines()

        matched_files = []
        for result_file in result_files:
            if os.path.isfile(result_file):
                try:
                    with open(result_file, 'r') as file:
                        content = file.read()
                        if all(filter_line in content for filter_line in filters):
                            matched_files.append(result_file)
                except PermissionError:
                    print(f"Permission denied: {result_file}")
                    matched_files.append(result_file)  # Add to matches despite permission denied
                except Exception as e:
                    print(f"An error occurred while reading file '{result_file}': {e}")

        if matched_files:
            print("Files containing all filter lines:")
            for matched_file in matched_files:
                print(matched_file)
        else:
            print("No files matched all filter lines.")
    except Exception as e:
        print(f"An error occurred while processing filters or results: {e}")

def main():
    names = read_names_from_file('searches.txt')
    results_file_path = os.path.join('results', 'results.txt')
    if names:  # Only proceed if names were successfully read
        search_for_names(names, results_file_path)
        read_filters_and_search_contents('filter.txt', results_file_path)

if __name__ == "__main__":
    main()