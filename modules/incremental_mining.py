from river import cluster, anomaly, preprocessing, compose
import numpy as np


class IncrementalMiner:
    """增量数据挖掘模块"""

    def __init__(self, config):
        self.config = config
        self.cluster_model = None
        self.anomaly_model = None
        self.feature_pipeline = None
        self.initialize_models()

    def initialize_models(self):
        """初始化增量学习模型"""
        # 增量聚类模型 (DBSTREAM)
        self.cluster_model = cluster.DBSTREAM(
            clustering_threshold=self.config.MAX_DISTANCE / 1000,  # 转换为公里
            fading_factor=0.01,
            cleanup_interval=100,
            intersection_factor=0.5
        )

        # 增量异常检测模型 (HalfSpaceTrees)
        self.anomaly_model = anomaly.HalfSpaceTrees(
            n_trees=10,
            height=15,
            window_size=100,
            seed=42
        )

        # 特征提取流水线
        self.feature_pipeline = compose.Pipeline(
            preprocessing.MinMaxScaler(),
            feature_extraction.Agg(
                by=['mmsi'],
                how={
                    'speed': ['mean', 'std', 'max'],
                    'direction': ['mean', 'std'],
                    'distance': ['sum']
                },
                window_size=100
            )
        )

    def update_models(self, data_point):
        """使用新数据点更新模型"""
        # 提取特征
        features = self.feature_pipeline.transform_one(data_point)

        if features:
            # 转换为适合模型输入的格式
            feature_vector = np.array(list(features.values()))

            # 更新聚类模型
            self.cluster_model.learn_one(feature_vector)

            # 更新异常检测模型
            score = self.anomaly_model.score_one(feature_vector)
            self.anomaly_model.learn_one(feature_vector)

            return self.cluster_model.predict_one(feature_vector), score
        return None, None

    def detect_anomaly(self, score):
        """检测异常点"""
        return score > self.config.ANOMALY_THRESHOLD

    def get_clusters(self):
        """获取当前聚类结果"""
        return self.cluster_model.clusters

    def get_common_routes(self):
        """提取常见航线模式"""
        # 简化的实现 - 实际应从聚类中提取模式
        common_routes = {}
        for cluster_id, cluster_info in self.cluster_model.clusters.items():
            common_routes[cluster_id] = {
                'avg_speed': cluster_info.center[0],
                'avg_direction': cluster_info.center[1],
                'size': cluster_info.n
            }
        return common_routes