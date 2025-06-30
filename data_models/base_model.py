class BaseDataModel:
    """所有数据模型的基类"""

    def __init__(self, config):
        self.config = config
        self.data = {}

    def load_data(self, source_type):
        """加载数据源"""
        # 实际应用中应从数据库或文件加载
        print(f"Loading data for {source_type}")
        return {}

    def preprocess(self):
        """数据预处理"""
        print("Preprocessing data")
        return self

    def to_dataframe(self):
        """转换为DataFrame格式"""
        import pandas as pd
        return pd.DataFrame(self.data)