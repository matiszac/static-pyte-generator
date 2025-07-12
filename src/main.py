import sys
import shutil
import os
from pathlib import Path

from typing import List

from htmlnode import ParentNode, LeafNode
from markdown_blocks import markdown_to_html_node, markdown_to_blocks, block_to_block_type, block_to_html_node

def main():
    base_path = '/'
    if len(sys.argv) == 2:
        base_path = sys.argv[1]

    root = Path(__file__).resolve().parent.parent
    prepare_public_folder(root)

    dir_path_content = root / 'content'
    template_file_path = root / 'template.html'
    dest_dir_path = root / 'docs'

    generate_pages_recursive(dir_path_content, template_file_path, dest_dir_path, base_path)

# ---- main end

def generate_pages_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path, base_path):
    files = get_files(dir_path_content)
    md_files = [f for f in files if f.suffix == '.md']

    if len(md_files) == 0:
        return
    
    template = template_path.read_text()

    for md in md_files:
        md_content = md.read_text()
        title = extract_title(md_content)
        html_content = markdown_to_html_node(md_content).to_html() # <--
        dest_content = (
            template
            .replace('{{ Title }}', title)
            .replace('{{ Content }}', html_content)
            .replace('href="/', f'href="{base_path}')
            .replace('src="/', f'src="{base_path}')
        )



        relative_path_str = str(md.relative_to(dir_path_content)).replace('.md', '.html')
        destination_file_path = dest_dir_path / relative_path_str
        # JUST INCASE
        destination_file_path.parent.mkdir(parents=True, exist_ok=True)
        destination_file_path.write_text(dest_content)




def generate_page(source_path, template_path, destination_path):
    print(f'Generating page from: {source_path} -> to: {destination_path} % using: {template_path}')
    template_html = get_file_text_content(template_path)
    index_md_content = get_file_text_content(source_path)

    title = extract_title(index_md_content)
    index_md_html = markdown_to_html_node(index_md_content).to_html()

    template_html = template_html.replace('{{ Title }}', title).replace('{{ Content }}', index_md_html)
    with open(destination_path, mode='w', encoding='utf-8') as f:
        f.write(template_html)




def prepare_public_folder(root: Path):

    public_folder_path = root / 'docs'

    if public_folder_path.exists():
        print('public folder detected. deleting public folder and its contents.')
        shutil.rmtree(public_folder_path)

    print('creating public folder')
    os.mkdir(public_folder_path)

    static_folder_path = root / 'static'

    if static_folder_path.exists():
        print('static folder detected. copying contents of static folder to public folder.')

        folders = get_folders(static_folder_path)
        if len(folders) != 0:
            for folder in folders:
                relative_path = folder.relative_to(static_folder_path)
                destination_folder_path = public_folder_path / relative_path
                destination_folder_path.mkdir(parents=True, exist_ok=True)

        files = get_files(static_folder_path)
        if len(files) != 0:
            for file in files:
                relative_path = file.relative_to(static_folder_path)
                destination_file_path = public_folder_path / relative_path
                # JUSSSTTT incase
                destination_file_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(str(file), str(destination_file_path))

    content_folder_path = root / 'content'

    if content_folder_path.exists():
        folders = get_folders(content_folder_path)
        if len(folders) != 0:
            print('sub-directories found in content folder. creating sub-directories in public folder.')
            for folder in folders:
                relative_path = folder.relative_to(content_folder_path)
                destination_folder_path = public_folder_path / relative_path
                destination_folder_path.mkdir(parents=True, exist_ok=True)

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

def get_path_list(from_path: Path) -> List[Path]:
    if not from_path.exists():
        raise ValueError('Path does not exist')
    paths = list(from_path.iterdir())
    if len(paths) == 0:
        return []
    return paths

def get_folders(from_path: Path) -> List[Path]:
    paths = get_path_list(from_path)
    if len(paths) == 0:
        return []
    folder_paths = []
    for path in paths:
        if path.is_dir():
            nested_folders = get_folders(path)
            folder_paths = [*folder_paths, path, *nested_folders]
    return folder_paths

def get_files(from_path: Path) -> List[Path]:
    paths = get_path_list(from_path)
    if len(paths) == 0:
        return []
    file_paths = []
    for path in paths:
        if path.is_dir():
            nested_files = get_files(path)
            file_paths = [*file_paths, *nested_files]
            continue
        file_paths.append(path)
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
