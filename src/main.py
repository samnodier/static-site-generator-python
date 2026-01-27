import os
import sys
from pathlib import Path
import shutil
from htmlnode import markdown_to_html_node
from extractors import extract_title

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
            shutil.copy(path_to_item, dest_dir)
        else:
            # item is a directory, create the new directory and recursively call the function
            new_dir = os.path.join(dest_dir, item)
            os.mkdir(new_dir)
            copy_contents(path_to_item, new_dir)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown_file = f.read()
        f.close()
    with open(template_path, 'r') as f:
        template_file = f.read()
        f.close()
    html_content = markdown_to_html_node(markdown_file)
    content = html_content.to_html()
    page_title = extract_title(markdown_file)
    full_html_page = template_file.replace("{{ Title }}", page_title)
    full_html_page = full_html_page.replace("{{ Content }}", content)
    full_html_page = full_html_page.replace('href="/', f'href="{basepath}')
    full_html_page = full_html_page.replace('src="/', f'src="{basepath}')
    file_directory = os.path.dirname(dest_path)
    os.makedirs(file_directory, exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(full_html_page)
        f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        path_to_content_item = os.path.join(dir_path_content, item)
        path_to_dest_item = Path(dest_dir_path, item)
        if os.path.isfile(path_to_content_item):
            generate_page(path_to_content_item, template_path, path_to_dest_item.with_suffix(".html"), basepath)
        else:
            generate_pages_recursive(path_to_content_item, template_path, path_to_dest_item, basepath)

def main():
    source_dir = "static"
    destination_dir = "docs"

    # Grab the first cli argument
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[0]

    try:
        copy_contents(source_dir, destination_dir)
    except Exception as e:
        print(e)

    try:
        generate_pages_recursive("content", "template.html", "docs", basepath)
    except Exception as e:
        print(e)


main()
