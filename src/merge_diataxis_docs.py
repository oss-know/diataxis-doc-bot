import os
import shutil

from openai import OpenAI
from common.config import config
from common.contants import LOGGER
from src.llm import LLMManager
from src.read_file import analyze_md_files


def process(path, prompt_file,module):
    api_key = config['model']['api_key']
    base_url = config['model']['base_url']
    temperature = config['model']['step2_temperature']
    model_name = config['model']['model_name']

    llm = LLMManager(api_key, base_url)

    refactor_doc_list = []
    content_list = []
    index = 0
    refactor_doc_list = analyze_md_files(os.path.join(path, 'refactor'))
    with open(f'../prompt/{prompt_file}', 'r', encoding='utf-8') as f:
        prompt_content = f.read()
    for doc_name in refactor_doc_list:
        index += 1
        with open(f'{os.path.join(path, "refactor", doc_name)}', 'r' ,
                  encoding='utf-8') as f:
            doc_content = f.read()
            content_list.append({"role": "user", "content": f"{index} ：文档所属模块:{module},文档名字：{doc_name} 文档内容如下：\n{doc_content} "})
        print(doc_name, '.........................................')

    LOGGER.info(f"----- streaming request 内容来自{path} -----\n")
    messages = [
        {"role": "system",
         "content": "角色：你是一位擅长技术文档重构的人工智能助手，熟悉 Diataxis 文档架构（教程 指南 参考 解释）"},
        # {"role": "system",
        #  "content": "输出文件会存放在读取输入文件的step2文件夹下，注意输入输出文件的相对关系"},
        {"role": "system", "content": prompt_content},
    ]
    messages.extend(content_list)

    llm.call_llm(model_name, messages, temperature)
    llm.save(os.path.join(path, 'refactor', 'step2'), 'index.md')
    LOGGER.info('*' * 300)


if __name__ == '__main__':
    doc_repo_path = config['doc_repo']['doc_repo_path']
    prompt_file = config['prompt']['step2']
    module_name = config['doc_repo']['module']
    if not os.path.exists(os.path.join(doc_repo_path, 'refactor', 'step2')):
        os.makedirs(os.path.join(doc_repo_path, 'refactor', 'step2'))
    process(doc_repo_path, prompt_file, module_name)
