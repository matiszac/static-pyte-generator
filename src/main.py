import shutil
import os
from pathlib import Path
from htmlnode import ParentNode, LeafNode
from markdown_blocks import markdown_to_html_node

def main():
    root = '..' if 'main.py' in os.listdir(os.path.curdir) else '.'
    prepare_public_folder(root)
    
    dir_path_content = os.path.join(root, 'content')
    template_file_path = os.path.join(root, 'template.html')
    dest_dir_path = os.path.join(root, 'public')

    generate_pages_recursive(dir_path_content, template_file_path, dest_dir_path)




# ---- main end

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = list(map(lambda path: Path(path), get_files(dir_path_content)))
    md_files = list(filter(lambda file: file.suffix == '.md' , files))
    if not len(md_files) > 0:
        return
    template = Path(template_path).read_text()
    for md in md_files:
        md_content = md.read_text()
        title = extract_title(md_content)
        html_content = markdown_to_html_node(md_content).to_html()
        dest_content = template.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
        sub_folder = md.parent.name
        if sub_folder == 'content':
            dest_file = Path(os.path.join(dest_dir_path, 'index.html'))
        else:
            dest_folder = os.path.join(dest_dir_path, sub_folder)
            dest_file = Path(os.path.join(dest_folder, 'index.html'))
        dest_file.write_text(dest_content)

def generate_page(source_path, template_path, destination_path):
    print(f'Generating page from: {source_path} -> to: {destination_path} % using: {template_path}')
    template_html = get_file_text_content(template_path)
    index_md_content = get_file_text_content(source_path)

    title = extract_title(index_md_content)
    index_md_html = markdown_to_html_node(index_md_content).to_html()

    template_html = template_html.replace('{{ Title }}', title).replace('{{ Content }}', index_md_html)
    with open(destination_path, mode='w', encoding='utf-8') as f:
        f.write(template_html)

def prepare_public_folder(root):
    public_folder_path = os.path.join(root, 'public')
    if os.path.exists(public_folder_path):
        print('public folder detected. deleting public folder and its contents.')
        shutil.rmtree(public_folder_path)
    print('creating public folder')
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

    content_folder_path = os.path.join(root, 'content')
    if os.path.exists(content_folder_path):
        folders = get_folders(content_folder_path)
        if len(folders) != 0:
            print('sub-directories found in content folder. creating sub-directories in public folder.')
            for folder in folders:
                folder_name = folder.replace(content_folder_path+'/', '')
                destination_folder_path = os.path.join(public_folder_path, folder_name)
                os.mkdir(destination_folder_path)

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line.lstrip('# ').rstrip('\n')
    raise ValueError('h1 title not found')

def get_file_text_content(file_path):
    if not os.path.isfile(file_path):
        raise ValueError('Cannot open path to directory as file')
    if not os.path.exists(file_path):
        raise ValueError('File does not exist')
    file_content = ''
    with open(file_path, encoding='utf-8') as f:
            file_content = f.read()
    return file_content

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
