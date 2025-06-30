import pandas as pd
from geopy.distance import great_circle
from config.settings import Config
from data_models.base_model import BaseDataModel


class DataProcessor:
    """数据处理模块，负责加载和预处理数据"""

    def __init__(self, config):
        self.config = config

    def load_data(self, data_sources):
        """加载指定数据源"""
        data = {}
        for source in data_sources:
            # 根据数据源类型加载数据
            if source == "ais":
                data["ais"] = self.load_ais_data()
            elif source == "ocean_currents":
                data["currents"] = self.load_ocean_currents()
            elif source == "bio_sensors":
                data["bio"] = self.load_bio_sensors()
            # 其他数据源...
        return data

    def load_ais_data(self):
        """加载AIS船舶数据"""
        try:
            df = pd.read_csv(self.config.DATA_PATH + "sample_ais_data.csv")
            print(f"Loaded AIS data with {len(df)} records")
            return self.preprocess_ais(df)
        except FileNotFoundError:
            print("AIS data file not found, generating sample data...")
            return self.generate_sample_ais()

    def preprocess_ais(self, df):
        """预处理AIS数据"""
        # 转换时间戳
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values(['mmsi', 'timestamp'], inplace=True)

        # 计算速度和方向
        df['prev_lat'] = df.groupby('mmsi')['latitude'].shift(1)
        df['prev_lon'] = df.groupby('mmsi')['longitude'].shift(1)
        df['prev_time'] = df.groupby('mmsi')['timestamp'].shift(1)

        # 计算距离和时间差
        df['distance'] = df.apply(
            lambda row: great_circle((row['prev_lat'], row['prev_lon']),
                                     (row['latitude'], row['longitude'])).meters
            if not pd.isna(row['prev_lat']) else 0, axis=1)

        df['time_diff'] = (df['timestamp'] - df['prev_time']).dt.total_seconds()
        df['speed'] = df['distance'] / df['time_diff'].replace(0, 1)
        df['speed'] = df['speed'].fillna(0)

        # 计算方向
        df['direction'] = df.apply(
            lambda row: self.calculate_direction(row) if not pd.isna(row['prev_lat']) else 0,
            axis=1
        )

        return df.drop(['prev_lat', 'prev_lon', 'prev_time'], axis=1)

    def calculate_direction(self, row):
        """计算航行方向"""
        import math
        lon_diff = row['longitude'] - row['prev_lon']
        lat_diff = row['latitude'] - row['prev_lat']

        # 避免除零错误
        if abs(lat_diff) < 1e-6:
            return 90 if lon_diff > 0 else 270

        angle = math.degrees(math.atan(lon_diff / lat_diff))

        if lat_diff > 0:
            return angle % 360
        else:
            return (angle + 180) % 360

    def generate_sample_ais(self, num_points=1000):
        """生成样本AIS数据"""
        import numpy as np
        import datetime
        import pandas as pd

        vessels = [f"Vessel_{i}" for i in range(5)]
        timestamps = [datetime.datetime.now() - datetime.timedelta(minutes=i)
                      for i in range(num_points)]

        data = {
            'mmsi': np.random.choice(vessels, num_points),
            'timestamp': timestamps,
            'latitude': np.random.uniform(10, 50, num_points),
            'longitude': np.random.uniform(130, 160, num_points)
        }

        df = pd.DataFrame(data)
        return self.preprocess_ais(df)

    def load_ocean_currents(self):
        """加载海洋流数据"""
        # 简化的实现
        return {
            "currents": [
                {"lat": 35.0, "lon": 140.0, "u": 0.5, "v": 0.2},
                {"lat": 35.5, "lon": 140.5, "u": 0.3, "v": 0.4}
            ]
        }

    def load_bio_sensors(self):
        """加载生物传感器数据"""
        # 简化的实现
        return {
            "sensors": [
                {"id": "bio_001", "lat": 34.2, "lon": 138.7, "temp": 18.5, "salinity": 34.2},
                {"id": "bio_002", "lat": 34.5, "lon": 139.0, "temp": 19.1, "salinity": 34.0}
            ]
        }