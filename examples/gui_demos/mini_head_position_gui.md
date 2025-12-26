# mini_head_position_gui.py

## 作用

通过 GUI 滑块直接控制 Reachy Mini 头部的姿态（Roll/Pitch/Yaw 角度和 X/Y/Z 位置）。

## 使用方法

```bash
python gui_demos/mini_head_position_gui.py
```

## 配置

修改文件顶部的 `ROBOT_IP` 变量为你的机器人 IP 地址：

```python
ROBOT_IP = "192.168.137.225"
```

## GUI 控制

- **Roll (deg)**: 头部翻滚角（-45° ~ 45°）
- **Pitch (deg)**: 头部俯仰角（-45° ~ 45°）
- **Yaw (deg)**: 头部偏航角（-175° ~ 175°）
- **X / Y / Z (m)**: 头部位置偏移（米）
- **Body Yaw (deg)**: 身体偏航角度（-180° ~ 180°）

## 关闭

按 `Ctrl+C` 或直接关闭窗口即可退出。
