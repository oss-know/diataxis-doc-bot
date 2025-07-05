import os
import yaml

class YamlConfigLoader:
    def __init__(self, env_var="CONFIG", default_path="../common/config.yaml"):
        # 从环境变量中读取配置文件路径，如果没有就使用默认路径
        self.config_file = os.getenv(env_var, default_path)
        self.config = None
        self.load()

    def load(self) -> dict:
        # 判断文件是否存在
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"配置文件未找到: {self.config_file}")

        # 加载 YAML 文件内容
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"YAML 语法错误: {e}")
        except Exception as e:
            raise RuntimeError(f"读取配置文件失败: {e}")

        # 检查格式是否为字典类型
        if not isinstance(self.config, dict):
            raise TypeError(f"配置文件格式应为字典（key-value），但得到: {type(self.config)}")

        print(f"成功加载配置文件: {self.config_file}")




config = YamlConfigLoader().config

