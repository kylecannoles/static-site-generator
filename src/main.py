from os import mkdir, path, listdir
from shutil import rmtree, copy
from textnode import TextNode, TextType

def main():
    copy_static_to_public()

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

main()
