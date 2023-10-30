import os
import fnmatch
import difflib

def search_directories(directory, keyword):
    """
    Search for directories in the given directory and its subdirectories that match the keyword.

    :param directory: The directory to start the search from.
    :param keyword: The keyword to search for in the directory names.
    :return: A list of paths to the directories that match the keyword.
    """
    matches = []
    for root, dirnames, _ in os.walk(directory):
        best_matches = difflib.get_close_matches(keyword, dirnames, n=5, cutoff=0.6)
        for match in best_matches:
            matches.append(os.path.join(root, match))
    return matches

def search_files(directory, pattern='*', keyword=None):
    """
    Search for files in a directory and its subdirectories.

    :param directory: The directory to start the search from.
    :param pattern: The pattern to search for. Defaults to all files.
    :param keyword: The keyword to search for in the filenames. If None, all files matching the pattern are returned.
    :return: A list of paths to the files that match the pattern and keyword.
    """
    matches = []
    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            if keyword:
                best_match = difflib.get_close_matches(keyword, [filename], n=1, cutoff=0.6)
                if best_match:
                    matches.append(os.path.join(root, best_match[0]))
            else:
                matches.append(os.path.join(root, filename))
    return matches

if __name__ == '__main__':
    search_type = input("Enter 1 to search in a local folder using keywords, or 2 to search for a file pattern: ")
    search_directory = os.path.expanduser('~')  # Set to user's home directory
    
    if search_type == '1':
        directory_keyword = input("Enter a keyword to search for directories: ")
        directories = search_directories(search_directory, directory_keyword)
        if not directories:
            print("No matching directories found.")
            exit(1)
        print("Select a directory to search in:")
        for i, directory in enumerate(directories, start=1):
            print(f"{i}. {directory}")
        selected_directory = int(input("Enter the number of the directory: "))
        search_directory = directories[selected_directory - 1]
        search_pattern = '*'
    elif search_type == '2':
        search_pattern = input("Enter the pattern to search for: ")
    else:
        print("Invalid option. Exiting.")
        exit(1)

    search_keyword = input("Enter a keyword to search for in the filenames (or leave blank to skip): ")
    results = search_files(search_directory, search_pattern, search_keyword)
    print(f"\nFound {len(results)} file(s):")
    for file in results:
        print(file)
