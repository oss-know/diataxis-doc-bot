import os
import shutil
from read_file import analyze_md_files


from common.config import config
from src.llm import LLMManager

model_name = config['model']['model_name']
api_key = config['model']['api_key']
base_url = config['model']['base_url']
temperature = config['model']['step1_temperature']
prompt_file = config['prompt']['step1']
doc_repo_path = config['doc_repo']['doc_repo_path']
output_version = '1'

def load_message(path, file_name, prompt_file):
    with open(os.path.join(path, file_name), 'r', encoding='utf-8') as f:
        doc_content = f.read()
    with open(f'../prompt/{prompt_file}', 'r', encoding='utf-8') as f:
        prompt_content = f.read()
    print(f"----- streaming request 内容来自{os.path.join(path, file_name)} -----")
    messages = [
        {"role": "system", "content": prompt_content},
        {"role": "user",
         "content": f"要求代码部分再原样给出不要做修改，原理部分也是尽量原文给出，请按照要求改写，文档内容如下：\n{doc_content} "},
    ]
    return messages


def process(path, file_name, prompt_file):
    messages = load_message(path, file_name, prompt_file)
    llm = LLMManager(api_key, base_url)
    llm.call_llm(model_name, messages, temperature)
    llm.save(os.path.join(path, "refactor"), file_name)


def run():
    path = doc_repo_path
    file_names = analyze_md_files(path)[:3]
    src_dir = os.path.join(path, 'figures')
    dst_dir = os.path.join(path, 'refactor', 'figures')
    if not os.path.exists(os.path.join(path, 'refactor')):
        os.makedirs(os.path.join(path, 'refactor'))

    if os.path.exists(os.path.join(path, 'figures')) and not os.path.exists(dst_dir):

        # os.makedirs(os.path.join(path, 'refactor', 'figures'))
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
        print('已成功复制到目录')

    for file_name in file_names:
        process(path, file_name,  prompt_file)
if __name__ == '__main__':

    run()
