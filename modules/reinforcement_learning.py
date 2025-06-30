import numpy as np
import gym
from gym import spaces


class ShippingRouteEnv(gym.Env):
    """航运路线优化环境"""

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.current_step = 0
        self.max_steps = config.RL_MAX_STEPS

        # 定义观测空间：位置、天气、燃油、时间
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0]),
            high=np.array([1, 1, 1, 100, 100]),
            dtype=np.float32
        )

        # 定义动作空间：航向、速度
        self.action_space = spaces.Box(
            low=np.array([0, 5]),  # 航向(0-360度), 速度(5-20节)
            high=np.array([360, 20]),
            dtype=np.float32
        )

        # 初始状态
        self.state = self.reset()

    def reset(self):
        """重置环境"""
        self.current_step = 0
        self.state = np.array([0.2, 0.5, 0.3, 50, 0])  # [位置x, 位置y, 天气, 燃油, 时间]
        return self.state

    def step(self, action):
        """执行动作"""
        heading, speed = action

        # 更新位置
        self.state[0] += np.cos(np.radians(heading)) * speed * 0.01
        self.state[1] += np.sin(np.radians(heading)) * speed * 0.01

        # 更新状态
        self.state[3] -= speed * 0.1  # 燃油消耗
        self.state[4] += 1  # 时间增加

        # 计算奖励
        reward = self.calculate_reward()

        # 检查是否完成
        self.current_step += 1
        done = self.current_step >= self.max_steps or self.state[3] <= 0

        return self.state, reward, done, {}

    def calculate_reward(self):
        """计算奖励函数"""
        # 距离目标越近奖励越高
        target_pos = np.array([0.8, 0.8])
        current_pos = np.array([self.state[0], self.state[1]])
        distance = np.linalg.norm(target_pos - current_pos)

        # 燃油效率奖励
        fuel_efficiency = 10 / (self.state[3] + 1e-5)

        # 时间惩罚
        time_penalty = -0.01 * self.state[4]

        # 天气惩罚
        weather_penalty = -0.1 * self.state[2]

        return 10 / (distance + 1) + fuel_efficiency + time_penalty + weather_penalty


class RoutingOptimizer:
    """航运路线优化模块"""

    def __init__(self, config):
        self.config = config
        self.env = ShippingRouteEnv(config)

    def optimize_route(self):
        """优化航运路线"""
        # 简化的实现 - 实际应使用强化学习算法
        route = []
        state = self.env.reset()

        for _ in range(self.env.max_steps):
            # 随机动作 (实际应使用训练好的策略)
            action = np.array([
                np.random.uniform(0, 360),
                np.random.uniform(5, 20)
            ])

            state, _, done, _ = self.env.step(action)
            route.append({
                "x": state[0],
                "y": state[1],
                "fuel": state[3],
                "time": state[4]
            })
            if done:
                break

        return route

    def process(self, data):
        """处理数据并优化路线"""
        return {
            "optimized_route": self.optimize_route(),
            "efficiency_improvement": 0.18  # 模拟18%效率提升
        }