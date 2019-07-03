import os


# this will make a list of all the files in the passed directory and subdirectories
def list_files(path_to_dir):
    all_files = list()
    if not os.path.isdir(path_to_dir):
        print("The given path was not to a directory.")
        return all_files
    list_of_file = os.listdir(path_to_dir)
    for fileName in list_of_file:
        full_path = os.path.join(path_to_dir, fileName)
        if os.path.isdir(full_path):
            all_files = all_files + list_files(full_path)
        else:
            all_files.append(full_path)
    return all_files
