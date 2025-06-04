import os.path
import wget
from common.config import config
from common.contants import LOGGER
from git import Repo
import re

def download_file(base_url='',module_type='', output_path='../docs'):
    if not base_url:
        raise Exception('url is empty')

    file_name = base_url.split('/')[-1]
    if module_type:
        if not os.path.exists(os.path.join(output_path, module_type)):
            os.makedirs(os.path.join(output_path, module_type))

    if os.path.exists(os.path.join(output_path, module_type, file_name)):
        LOGGER.warning('文件已存在')
        return
    filename = wget.download(base_url, out=os.path.join(output_path, module_type))
    LOGGER.info(f"\n 文件已下载为: {filename}")




# file_base_url = config['doc_repo']['base_url']
# module_type = config['doc_repo']['module_type']
# download_file(base_url=file_base_url, module_type=module_type)


def clone_git_repo(repo_url=''):

    # 克隆目标仓库
    repo_url = "https://gitee.com/openeuler/openstack-docs"
    base_path = '../docs'
    target_path = os.path.join(base_path, repo_url.split('/')[-2], repo_url.split('/')[-1])
    print('开始克隆项目')
    Repo.clone_from(repo_url, target_path)
    print("项目克隆完成！")


def clone_specific_version(repo_url, branch_or_tag, clone_dir):
    download_dir = clone_dir
    if os.path.exists(download_dir):
        print(f"目录已存在：{download_dir}")
        return

    print(f"正在克隆仓库：{repo_url} @ {branch_or_tag}")
    Repo.clone_from(repo_url, download_dir, branch=branch_or_tag, single_branch=True)


def parse_repo_branch(url):

    if '/blob/' in url:
        match = re.search(r'blob/([^/]+)/', url)
        # match = re.search(r'([^/]+)/blob', url)
        base_url = url.split('/blob/')[0]
    elif '/raw/' in url:
        match = re.search(r'raw/([^/]+)/', url)
        # match = re.search(r'([^/]+)/blob', url)
        base_url = url.split('/raw/')[0]
    else:
        return ''
    if match:
        version = match.group(1)
        print(f"基础链接：{base_url},版本号为:, {version}")

        return (base_url,version)
    else:
        return ''

from common.config import config

origin_url = config['doc_repo']['base_url']
print(origin_url)
repo_url, branch = parse_repo_branch(origin_url)
repo_name = repo_url.split('/')[-1].split('.')[0] if repo_url.split('/')[-1].endswith('.git') else repo_url.split('/')[-1]
current_dir = os.path.dirname(os.path.abspath(__file__))

clone_dir = f"{current_dir}/../docs/{repo_url.split('/')[-2]}/{repo_name}_{branch}"
clone_specific_version(repo_url, branch, clone_dir)

