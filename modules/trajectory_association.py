import numpy as np
from geopy.distance import great_circle
from config.settings import Config
from fastdtw import fastdtw


class TrajectoryAssociator:
    """轨迹关联分析模块"""

    def __init__(self, config):
        self.config = config

    def calculate_similarity(self, traj1, traj2):
        """计算两条轨迹的相似度"""
        # 空间相似度 (DTW距离)
        points1 = np.array(traj1['points'])
        points2 = np.array(traj2['points'])

        # 使用动态时间规整计算距离
        distance, _ = fastdtw(points1, points2, dist=lambda x, y: great_circle(x, y).meters)

        # 时间相似度 (时间窗口重叠)
        time_overlap = self._calculate_time_overlap(traj1['timestamps'], traj2['timestamps'])

        # 方向相似度
        dir_similarity = self._calculate_direction_similarity(traj1['directions'], traj2['directions'])

        # 组合相似度
        spatial_sim = 1 / (1 + distance / 1000)  # 归一化
        time_sim = time_overlap
        direction_sim = dir_similarity

        # 加权综合相似度
        total_similarity = 0.5 * spatial_sim + 0.3 * time_sim + 0.2 * direction_sim
        return total_similarity

    def _calculate_time_overlap(self, timestamps1, timestamps2):
        """计算时间重叠度"""
        if not timestamps1 or not timestamps2:
            return 0.0

        start1, end1 = min(timestamps1), max(timestamps1)
        start2, end2 = min(timestamps2), max(timestamps2)

        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)

        if overlap_start > overlap_end:
            return 0.0

        overlap_duration = (overlap_end - overlap_start).total_seconds()
        total_duration = (max(end1, end2) - min(start1, start2)).total_seconds()

        return overlap_duration / total_duration if total_duration > 0 else 0.0

    def _calculate_direction_similarity(self, dirs1, dirs2):
        """计算方向相似度"""
        if len(dirs1) == 0 or len(dirs2) == 0:
            return 0.0

        # 使用余弦相似度计算方向一致性
        dir_vec1 = np.array([np.cos(np.radians(d)) for d in dirs1])
        dir_vec2 = np.array([np.cos(np.radians(d)) for d in dirs2])

        # 计算方向序列相似度
        dot_product = np.dot(dir_vec1, dir_vec2)
        norm1 = np.linalg.norm(dir_vec1)
        norm2 = np.linalg.norm(dir_vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def associate_trajectories(self, trajectories):
        """关联轨迹并聚类"""
        clusters = []
        traj_ids = list(trajectories.keys())

        for i, id1 in enumerate(traj_ids):
            matched = False
            for cluster in clusters:
                for id2 in cluster:
                    similarity = self.calculate_similarity(trajectories[id1], trajectories[id2])
                    if similarity > self.config.SIMILARITY_THRESHOLD:
                        cluster.append(id1)
                        matched = True
                        break
                if matched:
                    break

            if not matched:
                clusters.append([id1])

        return clusters