# diataxis-doc-bot
Explore applying diataxis documentation theory to AI models

# 依赖
```shell
# 根目录
pip install -r requirements.txt

```

# config
```
修改配置文件
项目根目录/common/config.yaml

如：
doc_repo:
  base_url: https://gitee.com/openeuler/openstack-docs/blob/openEuler-25.03/docs/zh/install/antelope.md
  doc_repo_path: xx/docs/zh/install
  module: install
```

# download
```
执行
src/doc_repo_download.py
```

# step1 + step2
```
# 单文档重构
src/diataxis_rewrite.py
+
# 链接提取合并
src/merge_diataxis_docs.py

```
