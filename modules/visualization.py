import folium
import plotly.express as px
import pandas as pd


class Visualizer:
    """数据可视化模块"""

    def __init__(self, config):
        self.config = config

    def generate_dashboard(self, results, dashboard_type):
        """根据类型生成可视化仪表盘"""
        if dashboard_type == "bio_dashboard":
            return self.create_bio_dashboard(results)
        elif dashboard_type == "fishery_dashboard":
            return self.create_fishery_dashboard(results)
        elif dashboard_type == "iot_dashboard":
            return self.create_iot_dashboard(results)
        elif dashboard_type == "kg_dashboard":
            return self.create_kg_dashboard(results)
        elif dashboard_type == "maintenance_dashboard":
            return self.create_maintenance_dashboard(results)
        elif dashboard_type == "routing_dashboard":
            return self.create_routing_dashboard(results)
        else:
            return self.create_default_dashboard()

    def create_routing_dashboard(self, results):
        """航运优化仪表盘"""
        route_df = pd.DataFrame(results.get("optimized_route", []))

        if not route_df.empty:
            # 创建优化路线图
            fig = px.line_mapbox(
                route_df,
                lat="y",
                lon="x",
                zoom=3,
                title="Optimized Shipping Route"
            )
            fig.update_layout(mapbox_style="open-street-map")
            fig.write_html("results/routing_map.html")

        # 资源消耗图
        if "fuel" in route_df.columns:
            resource_fig = px.line(
                route_df,
                x="time",
                y="fuel",
                title="Fuel Consumption"
            )
            resource_fig.write_html("results/fuel_consumption.html")

        # 创建Folium地图作为主仪表盘
        map_center = [
            (self.config.MAP_BOUNDS[0] + self.config.MAP_BOUNDS[1]) / 2,
            (self.config.MAP_BOUNDS[2] + self.config.MAP_BOUNDS[3]) / 2
        ]
        dashboard = folium.Map(location=map_center, zoom_start=5)

        # 添加路线到地图
        if not route_df.empty:
            route_points = list(zip(route_df['y'], route_df['x']))
            folium.PolyLine(route_points, color="blue", weight=2.5, opacity=1).add_to(dashboard)

        return dashboard

    def create_maintenance_dashboard(self, results):
        """预测维护仪表盘"""
        warnings = results.get("warnings", [])

        # 创建警告表格
        if warnings:
            df = pd.DataFrame(warnings)
            fig = px.bar(df, x='component', y='risk', title='Maintenance Risk Assessment')
            fig.write_html("results/maintenance_risk.html")

        # 创建Folium地图
        map_center = [
            (self.config.MAP_BOUNDS[0] + self.config.MAP_BOUNDS[1]) / 2,
            (self.config.MAP_BOUNDS[2] + self.config.MAP_BOUNDS[3]) / 2
        ]
        dashboard = folium.Map(location=map_center, zoom_start=5)

        return dashboard

    def create_default_dashboard(self):
        """默认仪表盘"""
        map_center = [
            (self.config.MAP_BOUNDS[0] + self.config.MAP_BOUNDS[1]) / 2,
            (self.config.MAP_BOUNDS[2] + self.config.MAP_BOUNDS[3]) / 2
        ]
        return folium.Map(location=map_center, zoom_start=5)

    # 其他仪表盘创建方法类似...