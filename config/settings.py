class Config:
    """全局配置类，包含所有模块的默认设置"""

    # 数据参数
    DATA_PATH = "data/"
    DEFAULT_DATA_SOURCES = ["ais", "ocean_currents"]

    # 轨迹关联参数
    MAX_DISTANCE = 500  # 米
    TIME_WINDOW = 60  # 秒
    SIMILARITY_THRESHOLD = 0.7

    # 增量挖掘参数
    MIN_SUPPORT = 0.1
    WINDOW_SIZE = 1000  # 事务数
    SLIDE_SIZE = 100  # 滑动窗口大小

    # 异常检测参数
    ANOMALY_THRESHOLD = 3.0  # 标准差阈值

    # 可视化参数
    MAP_BOUNDS = [10, 50, 130, 160]  # 地图边界 [lat_min, lat_max, lon_min, lon_max]

    # 强化学习参数
    RL_MAX_STEPS = 100
    RL_LEARNING_RATE = 0.0003

    # 预测性维护参数
    PM_WARNING_THRESHOLD = 0.8