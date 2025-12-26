# Reachy Mini 完整 API 接口开发指南

本文档按通信协议分类详细说明 Reachy Mini 机器人的所有控制接口，包括所有参数范围、可控制自由度和限制。

---

## 目录

1. [REST API 接口](#1-rest-api-接口)
2. [WebSocket 接口](#2-websocket-接口)
3. [Zenoh 协议接口](#3-zenoh-协议接口)
4. [BLE 蓝牙接口](#4-ble-蓝牙接口)
5. [附录](#5-附录)

---

## 1. REST API 接口

**基础 URL**: `http://192.168.137.225:8000`

**特点**: 基于 HTTP 的请求-响应模式，适用于单次命令、配置查询，延迟 20-50ms

### 1.1 运动控制 `/move`

#### 可控对象与参数范围

| 可控对象 | 参数 | 范围 | 单位 | 说明 |
|---------|-----|------|------|------|
| **头部姿态** | x | ±0.05 | 米 | 前后位置，向前为正 |
| | y | ±0.05 | 米 | 左右位置，向左为正 |
| | z | -0.03 ~ +0.08 | 米 | 上下位置，向上为正 |
| | roll | ±25 | 度 | 翻滚角，右倾为正 |
| | pitch | ±35 | 度 | 俯仰角，抬头为正 |
| | yaw | ±160 | 度 | 偏航角，左转为正 |
| **天线** | antennas[0] | -80 ~ +80 | 度 | 左天线角度 |
| | antennas[1] | -80 ~ +80 | 度 | 右天线角度 |
| **身体** | body_yaw | -160 ~ +160 | 度 | 身体偏航角 |
| **运动参数** | duration | 0.1 ~ 10.0 | 秒 | 运动时长 |

**插值方式**:
- `linear`: 线性插值，匀速运动
- `minjerk`: 最小抖动插值，平滑运动（推荐）
- `ease`: 缓动插值，加减速平滑
- `cartoon`: 卡通插值，弹性效果

#### 接口列表

**POST `/move/goto`** - 平滑运动到目标（支持插值）

请求体示例:
```json
{
  "head_pose": {"x": 0, "y": 0, "z": 0.05, "roll": 0, "pitch": 15, "yaw": 0},
  "antennas": [30, -30],
  "body_yaw": 0,
  "duration": 2.0,
  "interpolation": "minjerk"
}
```

响应:
```json
{"uuid": "123e4567-e89b-12d3-a456-426614174000"}
```

---

**POST `/move/set_target`** - 立即设置目标（无轨迹）

请求体示例:
```json
{
  "target_head_pose": {
    "position": {"x": 0.0, "y": 0.0, "z": 0.0},
    "rotation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
  },
  "target_antennas": [0.0, 0.0],
  "target_body_yaw": 0.0
}
```

---

**POST `/move/goto_joint_positions`** - 关节空间运动

| 可控对象 | 参数 | 范围 | 单位 | 说明 |
|---------|-----|------|------|------|
| **头部关节** | head_joint_positions[0] | ±2.79 | 弧度 | yaw_body (-160°~+160°) |
| | head_joint_positions[1] | -0.84 ~ +1.40 | 弧度 | roll_sp_1 (-48°~+80°) |
| | head_joint_positions[2] | -0.84 ~ +1.40 | 弧度 | roll_sp_2 (-48°~+80°) |
| | head_joint_positions[3] | -0.84 ~ +1.40 | 弧度 | roll_sp_3 (-48°~+80°) |
| | head_joint_positions[4] | -1.22 ~ +1.40 | 弧度 | pitch_sp_1 (-70°~+80°) |
| | head_joint_positions[5] | -0.84 ~ +1.40 | 弧度 | pitch_sp_2 (-48°~+80°) |
| | head_joint_positions[6] | -1.22 ~ +1.40 | 弧度 | pitch_sp_3 (-70°~+80°) |
| **天线关节** | antennas_joint_positions[0] | ±1.40 | 弧度 | 左天线 (-80°~+80°) |
| | antennas_joint_positions[1] | ±1.40 | 弧度 | 右天线 (-80°~+80°) |

---

**POST `/move/play/wake_up`** - 唤醒动画

**POST `/move/play/goto_sleep`** - 休眠动画

**POST `/move/play/recorded-move-dataset/{dataset}/{move}`** - 播放预设动作
- 示例: `/move/play/recorded-move-dataset/pollen-robotics/reachy-mini-dances-library/another_one_bites_the_dust`

**GET `/move/running`** - 获取运行中的运动

**POST `/move/stop`** - 停止运动

---

### 1.2 状态查询 `/state`

#### 可查询对象

| 查询对象 | 接口 | 返回数据 | 值域 |
|---------|-----|---------|------|
| **头部姿态** | GET `/state/present_head_pose` | x, y, z, roll, pitch, yaw | 见 1.1 节范围 |
| **身体偏航** | GET `/state/present_body_yaw` | 弧度值 | -2.79 ~ +2.79 |
| **天线位置** | GET `/state/present_antenna_joint_positions` | [左, 右] 弧度 | ±1.40 |
| **完整状态** | GET `/state/full` | 所有状态 | - |

**GET `/state/full` 查询参数**:
- `with_control_mode`: 控制模式（默认 true）
- `with_head_pose`: 当前头部姿态（默认 true）
- `with_target_head_pose`: 目标头部姿态（默认 false）
- `with_head_joints`: 头部关节角度（默认 false）
- `with_target_head_joints`: 目标关节角度（默认 false）
- `with_body_yaw`: 身体偏航（默认 true）
- `with_target_body_yaw`: 目标身体偏航（默认 false）
- `with_antenna_positions`: 天线位置（默认 true）
- `with_target_antenna_positions`: 目标天线位置（默认 false）
- `with_passive_joints`: 被动关节（默认 false）
- `use_pose_matrix`: 使用矩阵格式（默认 false）

---

### 1.3 电机控制 `/motors`

#### 可控对象

| 控制对象 | 参数 | 可选值 | 说明 |
|---------|-----|-------|------|
| **电机模式** | mode | `enabled` | 电机启用，刚性控制（mode 3） |
| | | `disabled` | 电机禁用，可手动移动（mode 0） |
| | | `gravity_compensation` | 重力补偿，保持姿态（mode 5） |

**接口列表**:

**GET `/motors/status`** - 获取电机状态

**POST `/motors/set_mode/{mode}`** - 设置电机模式

---

### 1.4 音频控制 `/volume`

#### 可控对象与参数范围

| 可控对象 | 参数 | 范围 | 默认值 | 单位 |
|---------|-----|------|-------|------|
| **音量** | volume | 0 ~ 100 | 50 | - |
| **麦克风音量** | volume | 0 ~ 100 | 50 | - |

**接口列表**:

**GET `/volume/current`** - 获取音量

**POST `/volume/set`** - 设置音量

**POST `/volume/test-sound`** - 播放测试音

**GET `/volume/microphone/current`** - 获取麦克风音量

**POST `/volume/microphone/set`** - 设置麦克风音量

---

### 1.5 应用管理 `/apps`

**GET `/apps/list-available`** - 列出可用应用

**POST `/apps/install`** - 安装应用
```json
{"source": "huggingface", "app_id": "pollen-robotics/reachy_mini_conversation_app"}
```

**POST `/apps/start-app/{app_name}`** - 启动应用

**POST `/apps/stop-current-app`** - 停止应用

**GET `/apps/current-app-status`** - 获取应用状态

---

### 1.6 运动学 `/kinematics`

**GET `/kinematics/info`** - 获取运动学信息

**引擎类型**:
- `AnalyticalKinematics`: 解析解（默认，最快）
- `PlacoKinematics`: 优化解（支持碰撞检测）
- `NNKinematics`: 神经网络（需要模型）

**GET `/kinematics/urdf`** - 获取 URDF 模型

**GET `/kinematics/stl/{filename}`** - 获取 STL 文件（3D 可视化）

---

### 1.7 守护进程 `/daemon`

**POST `/daemon/start`** - 启动守护进程

**POST `/daemon/stop`** - 停止守护进程

**POST `/daemon/restart`** - 重启守护进程

**GET `/daemon/status`** - 获取状态

---

## 2. WebSocket 接口

**特点**: 双向实时通信，延迟 <10ms，支持 60Hz+ 高频控制

### 2.1 实时控制 `/move/ws/set_target`

**连接**: `ws://192.168.137.225:8000/move/ws/set_target`

#### 可控对象与参数范围

| 可控对象 | 参数 | 范围 | 单位 | 说明 |
|---------|-----|------|------|------|
| **头部姿态** | position.x | ±0.05 | 米 | 前后位置 |
| | position.y | ±0.05 | 米 | 左右位置 |
| | position.z | -0.03 ~ +0.08 | 米 | 上下位置 |
| | rotation (四元数) | 单位四元数 | - | 姿态 |
| **天线** | target_antennas[0] | -80 ~ +80 | 度 | 左天线 |
| | target_antennas[1] | -80 ~ +80 | 度 | 右天线 |
| **身体** | target_body_yaw | -160 ~ +160 | 度 | 身体偏航 |

**发送消息格式**（60Hz+）:
```json
{
  "target_head_pose": {
    "position": {"x": 0.0, "y": 0.0, "z": 0.0},
    "rotation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
  },
  "target_antennas": [0.0, 0.0],
  "target_body_yaw": 0.0
}
```

**接收错误反馈**:
```json
{"status": "error", "detail": "error message"}
```

---

### 2.2 状态流 `/state/ws/full`

**连接**: `ws://192.168.137.225:8000/state/ws/full?frequency=30`

#### 查询参数与可控范围

| 参数 | 范围 | 默认值 | 说明 |
|-----|------|-------|------|
| frequency | 1 ~ 100 | 10 | 更新频率（Hz） |
| with_head_pose | true/false | true | 包含头部姿态 |
| with_head_joints | true/false | false | 包含关节角度 |
| with_antenna_positions | true/false | true | 包含天线位置 |
| use_pose_matrix | true/false | false | 使用矩阵格式 |

**接收消息**（持续流）:
```json
{
  "control_mode": "enabled",
  "head_pose": {"x": 0.0, "y": 0.0, "z": 0.0, "roll": 0.0, "pitch": 0.0, "yaw": 0.0},
  "body_yaw": 0.0,
  "antennas_position": [0.0, 0.0],
  "timestamp": "2025-12-26T10:00:00Z"
}
```

---

### 2.3 运动更新 `/move/ws/updates`

**连接**: `ws://192.168.137.225:8000/move/ws/updates`

#### 事件类型

| 事件类型 | 说明 |
|---------|------|
| `move_started` | 运动开始 |
| `move_completed` | 运动完成 |
| `move_failed` | 运动失败 |
| `move_cancelled` | 运动取消 |

**接收事件**:
```json
{
  "type": "move_started",
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "details": ""
}
```

---

## 3. Zenoh 协议接口

**特点**: SDK 主要通信方式，延迟 10-20ms，高带宽，支持高频控制

### 3.1 连接配置

**客户端模式（指定 IP）**:
```python
{"mode": "client", "connect": {"endpoints": ["tcp/192.168.137.225:7447"]}}
```

**对等模式（自动发现）**:
```python
{"mode": "peer", "scouting": {"multicast": {"enabled": true}}}
```

---

### 3.2 Topic 与可控对象

| Topic | 方向 | 可控/返回对象 | 数据类型 |
|-------|------|--------------|---------|
| `reachy_mini/command` | → | 头部姿态、天线、身体偏航、电机模式 | dict |
| `reachy_mini/joint_positions` | ← | 所有 9 个关节位置 | list |
| `reachy_mini/head_pose` | ← | 头部 4x4 姿态矩阵 | ndarray |
| `reachy_mini/daemon_status` | ← | 守护进程状态 | dict |
| `reachy_mini/task` | → | 任务请求 | dict |
| `reachy_mini/task_progress` | ← | 任务进度 | dict |
| `reachy_mini/recorded_data` | ← | 录制数据 | bytes |

---

### 3.3 命令格式与参数范围

#### 发送命令到 `reachy_mini/command`

**设置目标姿态**:
```python
{
    "head_pose": [[4x4 矩阵]],  # 头部姿态矩阵
    "antennas_joint_positions": [0.5, -0.5],  # 天线弧度 [-1.40, +1.40]
    "body_yaw": 0.0  # 身体偏航 弧度 [-2.79, +2.79]
}
```

**启用扭矩**:
```python
{"torque": True}
```

**启用重力补偿**:
```python
{"gravity_compensation": True}
```

---

### 3.4 返回数据格式

**关节位置** (`reachy_mini/joint_positions`):
```python
[
    yaw_body,      # [0] ±2.79 rad (±160°)
    roll_sp_1,     # [1] -0.84~+1.40 rad (-48°~+80°)
    roll_sp_2,     # [2] -0.84~+1.40 rad (-48°~+80°)
    roll_sp_3,     # [3] -0.84~+1.40 rad (-48°~+80°)
    pitch_sp_1,    # [4] -1.22~+1.40 rad (-70°~+80°)
    pitch_sp_2,    # [5] -0.84~+1.40 rad (-48°~+80°)
    pitch_sp_3,    # [6] -1.22~+1.40 rad (-70°~+80°)
    antenna_left,  # [7] ±1.40 rad (±80°)
    antenna_right  # [8] ±1.40 rad (±80°)
]
```

---

## 4. BLE 蓝牙接口

**特点**: 近距离配置、调试、应急控制，延迟 100-500ms

### 4.1 连接信息

| 项目 | 值 |
|-----|-----|
| **BLE 设备名称** | ReachyMini |
| **PIN 码获取** | 序列号后 5 位（`dfu-util -l` 查询） |

### 4.2 使用 nRF Connect 连接

1. 安装 nRF Connect (Android/iOS)
2. 扫描并连接 "ReachyMini" 设备
3. Unknown Service → WRITE 发送十六进制命令

### 4.3 可控命令与参数

| 命令 | 十六进制 | 说明 |
|-----|---------|------|
| **PIN 验证** | `50494E5F3030303033` | PIN_00033（替换为实际 PIN） |
| **查询状态** | `535441545553` | STATUS |
| **重置热点** | `434D445F484F5453504F54` | CMD_HOTSPOT |
| **重启守护进程** | `434D445F524553544152545F4441454D4F4E` | CMD_RESTART_DAEMON |
| **软件复位** | `434D445F534F4654574152455F5245534554` | CMD_SOFTWARE_RESET |

### 4.4 Web Bluetooth 工具

官方工具: https://pollen-robotics.github.io/reachy_mini/

支持 Chrome 内核浏览器，可直接通过网页连接蓝牙。

---

## 5. 附录

### 5.1 机器人自由度总览

| 部位 | 自由度数 | 关节名称 | 范围（度） | 范围（弧度） |
|-----|---------|---------|-----------|-------------|
| **头部** | 7 | yaw_body | ±160° | ±2.79 |
| | | roll_sp_1/2/3 | -48° ~ +80° | -0.84 ~ +1.40 |
| | | pitch_sp_1/2/3 | -70° ~ +80° | -1.22 ~ +1.40 |
| **天线** | 2 | 左天线 | ±80° | ±1.40 |
| | | 右天线 | ±80° | ±1.40 |
| **身体** | 1 | body_yaw | ±160° | ±2.79 |

**总计**: 10 个可控自由度

### 5.2 任务空间工作空间

| 轴 | 范围 | 单位 | 说明 |
|----|------|------|------|
| X（前后） | ±0.05 | 米 | 向前为正 |
| Y（左右） | ±0.05 | 米 | 向左为正 |
| Z（上下） | -0.03 ~ +0.08 | 米 | 向上为正 |
| Roll（翻滚） | ±25 | 度 | 右倾为正 |
| Pitch（俯仰） | ±35 | 度 | 抬头为正 |
| Yaw（偏航） | ±160 | 度 | 左转为正 |

### 5.3 使用场景推荐

| 场景 | 推荐接口 | 理由 |
|-----|---------|------|
| **实时跟踪控制** | WebSocket `/move/ws/set_target` | 60Hz+，低延迟 |
| **状态监控** | WebSocket `/state/ws/full` | 可调频率，完整数据 |
| **单次运动** | REST `/move/goto` | 简单可靠 |
| **Python 开发** | Zenoh SDK | 官方支持 |
| **Web 应用** | REST + WebSocket | 浏览器兼容 |
| **移动应用** | REST API | 标准 HTTP |
| **配置调试** | BLE | 近距离配置 |

### 5.4 姿态表示格式

#### 欧拉角格式（度）
```json
{"x": 0.0, "y": 0.0, "z": 0.0, "roll": 0.0, "pitch": 0.0, "yaw": 0.0}
```

#### 四元数格式
```json
{"position": {"x": 0.0, "y": 0.0, "z": 0.0}, "rotation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}}
```

#### 4x4 矩阵格式（扁平化）
```json
{"m": [r11, r12, r13, x, r21, r22, r23, y, r31, r32, r33, z, 0, 0, 0, 1]}
```

### 5.5 注意事项

1. **坐标系**: 右手坐标系，X 轴向前，Z 轴向上
2. **角度单位**: API 使用度，内部使用弧度
3. **安全限制**: 所有关节都有软件/硬件限位保护
4. **电机保护**: 避免长时间在极限位置
5. **网络延迟**: WebSocket <10ms，REST 20-50ms
6. **控制频率**: 建议不超过 60Hz，避免命令拥塞
7. **优先级**: 运动中的 goto 命令会被忽略（需先 stop）

---

## 示例代码

### JavaScript 实时控制

```javascript
const controlWS = new WebSocket('ws://192.168.137.225:8000/move/ws/set_target');
const stateWS = new WebSocket('ws://192.168.137.225:8000/state/ws/full?frequency=60');

// 实时控制（60Hz）
function setHeadPose(x, y, z, roll, pitch, yaw) {
  const command = {
    target_head_pose: {
      position: { x, y, z },
      rotation: eulerToQuaternion(roll, pitch, yaw)
    }
  };
  controlWS.send(JSON.stringify(command));
}

// 状态回调
stateWS.onmessage = (event) => {
  const state = JSON.parse(event.data);
  console.log('头部位置:', state.head_pose);
};
```

### Python 平滑运动

```python
import requests

# 平滑运动到目标
data = {
    "head_pose": {"x": 0, "y": 0, "z": 0.05, "roll": 0, "pitch": 15, "yaw": 0},
    "antennas": [30, -30],
    "body_yaw": 0,
    "duration": 2.0,
    "interpolation": "minjerk"
}
response = requests.post('http://192.168.137.225:8000/move/goto', json=data)
print(f"运动 UUID: {response.json()['uuid']}")
```

### Python 状态查询

```python
import requests

response = requests.get('http://192.168.137.225:8000/state/full')
state = response.json()

print(f"头部姿态: {state['head_pose']}")
print(f"天线位置: {state['antennas_position']}")
print(f"控制模式: {state['control_mode']}")
```
