# Reachy Mini 🤖

[![在 HuggingChat 上提问](https://img.shields.io/badge/Ask_on-HuggingChat-yellow?logo=huggingface&logoColor=yellow&style=for-the-badge)](https://huggingface.co/chat/?attachments=https%3A%2F%2Fgist.githubusercontent.com%2FFabienDanieau%2F919e1d7468fb16e70dbe984bdc277bba%2Fraw%2Fdoc_reachy_mini_full.md&prompt=Read%20this%20documentation%20about%20Reachy%20Mini%20so%20I%20can%20ask%20questions%20about%20it.)
[![Discord](https://img.shields.io/badge/Discord-加入社区-7289DA?logo=discord&logoColor=white)](https://discord.gg/Y7FgMqHsub)

**Reachy Mini 是一个开源的、富有表现力的机器人，专为黑客和 AI 构建者设计。**

🛒 [**购买 Reachy Mini**](https://www.hf.co/reachy-mini/)

[![Reachy Mini Hello](/docs/assets/reachy_mini_hello.gif)](https://www.pollen-robotics.com/reachy-mini/)

## ⚡️ 构建并启动你的机器人

**选择你的平台查看详细指南：**

| **🤖 Reachy Mini (无线版)** | **🔌 Reachy Mini Lite** | **💻 仿真** |
| :---: | :---: | :---: |
| 完整的自主体验。<br>树莓派 4 + 电池 + WiFi。 | 开发者版本。<br>USB 连接电脑。 | 无需硬件。<br>在 MuJoCo 中原型开发。 |
| 👉 [**无线版指南**](docs/platforms/reachy_mini/get_started.md) | 👉 [**Lite 版指南**](docs/platforms/reachy_mini_lite/get_started.md) | 👉 [**仿真指南**](docs/platforms/simulation/get_started.md) |



> ⚡ **专业提示**：安装 [uv](https://docs.astral.sh/uv/getting-started/installation/) 可获得 10-100 倍的应用安装速度（自动检测，回退到 `pip`）。

<br>

## 📱 应用与生态系统

Reachy Mini 内置由 Hugging Face Spaces 驱动的应用商店。你可以直接从机器人仪表板一键安装这些应用！

* **🗣️ [对话应用](https://huggingface.co/spaces/pollen-robotics/reachy_mini_conversation_app)**：与 Reachy Mini 自然对话（由 LLM 驱动）。
* **📻 [收音机](https://huggingface.co/spaces/pollen-robotics/reachy_mini_radio)**：与 Reachy Mini 一起听收音机！
* **👋 [手势追踪](https://huggingface.co/spaces/pollen-robotics/hand_tracker_v2)**：机器人实时跟随你的手部动作。

👉 [**在 Hugging Face 上浏览所有应用**](https://hf.co/reachy-mini/#/apps)

<br>

## 🚀 Reachy Mini SDK 快速入门

### 快速预览
只需 **几行代码** 即可控制机器人：

```python
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

with ReachyMini() as mini:
    # 抬头并倾斜头部
    mini.goto_target(
        head=create_head_pose(z=10, roll=15, degrees=True, mm=True),
        duration=1.0
    )
```

### 用户指南
* **[安装](docs/SDK/installation.md)**：5 分钟设置你的电脑
* **[快速入门指南](docs/SDK/quickstart.md)**：在 Reachy Mini 上运行你的第一个行为
* **[Python SDK](docs/SDK/python-sdk.md)**：学习移动、视觉、语音和听觉
* **[AI 集成](docs/SDK/integration.md)**：连接 LLM、构建应用并发布到 Hugging Face
* **[核心概念](docs/SDK/core-concept.md)**：架构、坐标系统和安全限制
* 🤗[**与社区分享你的应用**](https://huggingface.co/blog/pollen-robotics/make-and-publish-your-reachy-mini-apps)
* 📂 [**浏览示例文件夹**](examples)


<br>

## 🛠 硬件概览

Reachy Mini 机器人以套件形式出售，通常需要 **2 到 3 小时** 组装。详细的分步指南可在上述平台特定文件夹中找到。

* **Reachy Mini (无线版)**：机载运行（RPi 4），自主，包含 IMU。[查看规格](docs/platforms/reachy_mini/hardware.md)
* **Reachy Mini Lite**：在你的 PC 上运行，通过电源插座供电。[查看规格](docs/platforms/reachy_mini_lite/hardware.md)

<br>

## ❓ 故障排除

遇到问题？👉 **[查看故障排除与常见问题指南](/docs/troubleshooting.md)**

<br>

## 🤝 社区与贡献

* **加入社区**：加入 [Discord](https://discord.gg/2bAhWfXme9) 分享你的 Reachy 时刻，一起构建应用并获得帮助。
* **发现 bug？** 在此仓库中提交 issue。


## 许可证

本项目采用 Apache 2.0 许可证。详情请参见 [LICENSE](LICENSE) 文件。
硬件设计文件采用 Creative Commons BY-SA-NC 许可证。
