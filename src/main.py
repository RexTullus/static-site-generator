import os, shutil, sys

from generate_page import generate_pages_recursive

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    copy_recursive(src, dst)

def copy_recursive(src, dst):  
    for entry in os.listdir(src):
        source_path = os.path.join(src, entry)
        dest_path = os.path.join(dst, entry)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            os.mkdir(dest_path)
            copy_recursive(source_path, dest_path)
   
if __name__ == "__main__":
    main()