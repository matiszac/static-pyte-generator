import shutil
import os
from htmlnode import ParentNode, LeafNode
from markdown_blocks import markdown_to_html_node

test_text = '''# heading

* item 1
* item 2
* item 3

Some normal text *italic* now some `code` and **bold**.

1. yes
2. i
3. can

> i love
> programming

```
some code
```

## Heading 2


Click [here](https://google.com)'''

def main():
    root = '..' if 'main.py' in os.listdir(os.path.curdir) else '.'

    public_folder_path = os.path.join(root, 'public')

    if os.path.exists(public_folder_path):
        print('public folder detected. deleting public folder and its contents.')
        shutil.rmtree(public_folder_path)
    os.mkdir(public_folder_path)

    static_folder_path = os.path.join(root, 'static')
    if os.path.exists(static_folder_path):
        print('static folder detected. copying contents of static folder to public folder.')
        folders = get_folders(static_folder_path)
        if len(folders) != 0:
            for folder in folders:
                folder_name = folder.replace(static_folder_path+'/', '')
                destination_folder_path = os.path.join(public_folder_path, folder_name)
                os.mkdir(destination_folder_path)

        files = get_files(static_folder_path)
        if len(files) != 0:
            for file in files:
                file_name = file.replace(static_folder_path+'/', '')
                destination_file_path = os.path.join(public_folder_path, file_name)
                shutil.copy(file, destination_file_path)

def get_file_list(path):
    if path == '' or path == None:
        raise ValueError('Invalid path')
    if not os.path.exists(path):
        raise ValueError('Path does not exist')
    files = os.listdir(path)
    if len(files) == 0:
        return None
    return files

def get_folders(path):
    files = get_file_list(path)
    if files == None:
        return []
    folder_paths = []
    for file in files:
        file_path = os.path.join(path, file)
        if not os.path.isfile(file_path):
            nested_folders = get_folders(file_path)
            folder_paths = [*folder_paths, file_path, *nested_folders]
    return folder_paths

def get_files(path):
    files = get_file_list(path)
    if files == None:
        return []
    file_paths = []
    for file in files:
        file_path = os.path.join(path, file)
        if not os.path.isfile(file_path):
            nested_files = get_files(file_path)
            file_paths = [*file_paths, *nested_files]
            continue
        file_paths.append(file_path)
    return file_paths


def print_html_node_tree(html_node, padding):
    if html_node == None:
        return
    if isinstance(html_node, LeafNode):
        print(f"{padding}{html_node.tag} : {html_node.value}")
        return
    if isinstance(html_node, ParentNode):
        print(f"{html_node.tag} : ")
        for child in html_node.children:
            print_html_node_tree(child, padding+'  ')
    return


main()
