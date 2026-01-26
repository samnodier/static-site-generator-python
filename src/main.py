import os
import shutil

def copy_contents(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        raise Exception ("Source directory does not exist")
    if not os.path.exists(dest_dir):
        raise Exception ("Destination directory does not exist")
    # Remove the contents of the dest_dir
    shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    for item in os.listdir(source_dir):
        path_to_item = os.path.join(source_dir, item)
        if os.path.isfile(path_to_item):
            dest_path = shutil.copy(path_to_item, dest_dir)
        else:
            # item is a directory, create the new directory and recursively call the function
            new_dir = os.path.join(dest_dir, item)
            os.mkdir(new_dir)
            copy_contents(path_to_item, new_dir)


def main():
    source_dir = "static"
    destination_dir = "public"
    try:
        copy_contents(source_dir, destination_dir)
    except Exception as e:
        print(e)

main()
