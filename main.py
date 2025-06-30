import sys
import json
import importlib
from config.settings import Config
from config.research_profiles import RESEARCH_PROFILES


class AdaptiveAnalysisPlatform:
    """自适应分析平台主类"""

    def __init__(self, profile_name):
        self.config = Config()
        self.profile = RESEARCH_PROFILES.get(profile_name)
        if not self.profile:
            raise ValueError(f"Invalid research profile: {profile_name}")

        self.data_sources = self.profile["data_sources"]
        self.modules = {}
        self.results = {}

        # 加载研究方向特定配置
        self.load_profile_config(profile_name)

        # 初始化模块
        self.initialize_modules()

    def load_profile_config(self, profile_name):
        """加载研究方向特定配置"""
        try:
            with open(f"profiles/{profile_name}.json") as f:
                profile_config = json.load(f)
                # 更新全局配置
                for key, value in profile_config.items():
                    setattr(self.config, key, value)
        except FileNotFoundError:
            print(f"No specific config found for {profile_name}, using default settings")

    def initialize_modules(self):
        """动态加载所需模块"""
        for module_name in self.profile["modules"]:
            try:
                module = importlib.import_module(f"modules.{module_name}")
                # 调用模块的初始化函数
                module_class = getattr(module, module_name.capitalize())
                self.modules[module_name] = module_class(self.config)
                print(f"Initialized module: {module_name}")
            except (ImportError, AttributeError) as e:
                print(f"Error initializing module {module_name}: {str(e)}")

    def load_data(self):
        """根据配置加载数据"""
        # 初始化数据处理模块
        from modules.data_processing import DataProcessor
        processor = DataProcessor(self.config)
        return processor.load_data(self.data_sources)

    def process(self):
        """执行分析流程"""
        data = self.load_data()

        # 按顺序执行模块
        for module_name in self.profile["modules"]:
            if module_name == "data_processing":
                # 数据处理模块已经执行过
                continue

            print(f"Executing module: {module_name}")
            module = self.modules.get(module_name)
            if module:
                try:
                    result = module.process(data)
                    data.update(result)
                    self.results[module_name] = result
                except Exception as e:
                    print(f"Error processing module {module_name}: {str(e)}")

        return self.results

    def visualize(self):
        """生成可视化结果"""
        if "visualization" not in self.modules:
            from modules.visualization import Visualizer
            self.modules["visualization"] = Visualizer(self.config)

        dashboard = self.modules["visualization"].generate_dashboard(
            self.results,
            self.profile["visualization"]
        )

        # 保存仪表盘
        dashboard.save(f"results/{self.profile['visualization']}.html")
        print(f"Visualization saved to results/{self.profile['visualization']}.html")


def main():
    """主函数入口"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <profile_name>")
        print("Available profiles:")
        for profile in RESEARCH_PROFILES.keys():
            print(f"  - {profile}: {RESEARCH_PROFILES[profile]['name']}")
        sys.exit(1)

    profile_name = sys.argv[1]
    print(f"Starting analysis for profile: {profile_name}")

    try:
        # 初始化平台
        platform = AdaptiveAnalysisPlatform(profile_name)

        # 执行分析
        results = platform.process()
        print("Analysis completed successfully")

        # 生成可视化
        platform.visualize()

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()