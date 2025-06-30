RESEARCH_PROFILES = {
    "marine_bio": {
        "name": "海洋生物数据融合",
        "description": "分析海洋生物与环境因素的相互作用",
        "data_sources": ["bio_sensors", "environmental"],
        "modules": ["data_processing", "incremental_mining", "knowledge_graph"],
        "visualization": "bio_dashboard"
    },
    "fishery_monitoring": {
        "name": "渔业数据流监测",
        "description": "实时监测渔业活动并检测异常行为",
        "data_sources": ["vessel_tracking", "catch_reports"],
        "modules": ["data_processing", "incremental_mining", "trajectory_association"],
        "visualization": "fishery_dashboard"
    },
    "iot_stream": {
        "name": "海洋物联网流计算",
        "description": "处理海洋传感器网络产生的实时数据流",
        "data_sources": ["iot_sensors", "ocean_currents"],
        "modules": ["data_processing", "incremental_mining", "trajectory_association"],
        "visualization": "iot_dashboard"
    },
    "knowledge_evolution": {
        "name": "工业知识图谱演化",
        "description": "构建和演化工业设备知识图谱",
        "data_sources": ["maintenance_logs", "equipment_sensors"],
        "modules": ["data_processing", "knowledge_graph"],
        "visualization": "kg_dashboard"
    },
    "predictive_maintenance": {
        "name": "渔船预测性维护",
        "description": "预测渔船设备故障并推荐维护计划",
        "data_sources": ["vessel_sensors", "maintenance_logs"],
        "modules": ["data_processing", "predictive_maintenance"],
        "visualization": "maintenance_dashboard"
    },
    "routing_optimization": {
        "name": "航运强化学习优化",
        "description": "使用强化学习优化船舶航行路线",
        "data_sources": ["vessel_tracking", "weather", "port_data"],
        "modules": ["data_processing", "reinforcement_learning"],
        "visualization": "routing_dashboard"
    }
}