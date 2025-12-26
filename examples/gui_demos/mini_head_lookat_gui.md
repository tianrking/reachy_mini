# mini_head_lookat_gui.py

## 作用

通过 GUI 滑块控制 Reachy Mini 头部看向指定的 3D 坐标点 (X, Y, Z)。

## 使用方法

```bash
python gui_demos/mini_head_lookat_gui.py
```

## 配置

修改文件顶部的 `ROBOT_IP` 变量为你的机器人 IP 地址：

```python
ROBOT_IP = "192.168.137.225"
```

## GUI 控制

- **X / Y / Z (m)**: 控制头部看向的目标位置（米）
- **Body Yaw (deg)**: 控制身体偏航角度

## 关闭

按 `Ctrl+C` 或直接关闭窗口即可退出。
