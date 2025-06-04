import json
import markdown
import os

from bs4 import BeautifulSoup


def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def parse_headings(md_text):
    html = markdown.markdown(md_text, extensions=['extra'])
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])


def build_outline_tree(headings):
    root = {"title": "root", "level": 0, "children": []}
    stack = [{"node": root, "level": 0}]

    for heading in headings:
        cur_level = int(heading.name[1:])
        title = heading.text.strip()

        new_node = {"title": title, "level": cur_level, "children": []}

        # 弹出比当前层级高的节点
        while stack[-1]["level"] >= cur_level:
            stack.pop()

        # 添加到父级的 children 中
        stack[-1]["node"]["children"].append(new_node)
        stack.append({"node": new_node, "level": cur_level})

    return root["children"]


def save_outline_to_json(outline, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(outline, f, indent=4, ensure_ascii=False)


def generate_filename_from_heading(md_text):
    html = markdown.markdown(md_text, extensions=['extra'])
    soup = BeautifulSoup(html, 'html.parser')
    h1 = soup.find('h1')
    if h1:
        return h1.text.strip() + ".md"
    else:
        return "untitled.md"


def rename_md_files_in_dir(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                md_text = f.read()
            new_name = generate_filename_from_heading(md_text)
            new_path = os.path.join(directory, new_name)
            os.rename(file_path, new_path)
            print(f"Renamed {filename} -> {new_name}")
