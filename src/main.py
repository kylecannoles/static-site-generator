from os import mkdir, makedirs, path, listdir
from shutil import rmtree, copy

from textnode import TextNode, TextType
from mdparser import markdown_to_html_node, extract_title

def main():
    copy_static_to_public()
    generate_pages_recursive()

def copy_files(src,dest, file_list):
    for file in file_list:
        src_file_path = path.join(src,file)
        dest_file_path = path.join(dest,file)
        if path.isfile(src_file_path):
            copy(src_file_path, dest_file_path)
        else:
            mkdir(dest_file_path)
            copy_files(src_file_path, dest_file_path, listdir(src_file_path)) 

def copy_static_to_public(src="static", dest="public"):
    # Delete contents of public
    if path.exists(dest):
        rmtree(dest)
    # Create public folder
    mkdir("public")
    file_list = listdir(src)
    copy_files(src,dest, file_list)

def generate_page(from_path="content/index.md", template_path="template.html", dest_path="public/index.html"):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")
    # Read md file from dest_path
    f = open(from_path, "r")
    md_file = f.read()
    # Read template file from template_path
    f = open(template_path, "r")
    template_file = f.read()
    # Convert markdown to html_node 
    html_node = markdown_to_html_node(md_file)
    # Get page title
    page_title = extract_title(md_file)
    # Replace template variables
    html_file = template_file.replace("{{ Title }}", page_title).replace("{{ Content }}", html_node.to_html())
    # Make directories if needed
    d_path, f_name = path.split(dest_path)
    makedirs(d_path, exist_ok=True)
    # Write to file
    f = open(dest_path, "w")
    f.write(html_file)

def generate_pages_recursive(dir_path_content="content", template_path="template.html", dest_dir_path="public"):
    current_dir_files = listdir(dir_path_content)
    for file in current_dir_files:
        file_path = path.join(dir_path_content, file)
        if path.isfile(file_path):
            f_name, f_ext = path.splitext(file)
            generate_page(file_path, template_path, path.join(dest_dir_path, f_name + ".html"))
        else:
            makedirs(file_path, exist_ok=True)
            generate_pages_recursive(file_path, template_path, path.join(dest_dir_path,file))

main()
