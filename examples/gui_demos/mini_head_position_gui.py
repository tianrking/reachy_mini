"""Reachy Mini Head Position GUI Example."""

import json
import time
import tkinter as tk

import numpy as np
import zenoh
from scipy.spatial.transform import Rotation as R

from reachy_mini import ReachyMini
from reachy_mini.io.zenoh_client import ZenohClient
from reachy_mini.media.media_manager import MediaBackend, MediaManager
from reachy_mini.utils import create_head_pose


ROBOT_IP = "192.168.137.225"


def main():
    """Run a GUI to set the head position and orientation of Reachy Mini."""
    # 创建自定义 Zenoh 客户端连接到指定 IP
    zc = zenoh.Config.from_json5(
        json.dumps(
            {"mode": "client", "connect": {"endpoints": [f"tcp/{ROBOT_IP}:7447"]}}
        )
    )
    client = ZenohClient("reachy_mini", localhost_only=False)
    # 替换客户端的 session 为自定义配置
    client.session.close()
    client.session = zenoh.open(zc)
    client.cmd_pub = client.session.declare_publisher(f"{client.prefix}/command")
    client.joint_sub = client.session.declare_subscriber(
        f"{client.prefix}/joint_positions",
        client._handle_joint_positions,
    )
    client.pose_sub = client.session.declare_subscriber(
        f"{client.prefix}/head_pose",
        client._handle_head_pose,
    )
    client.recording_sub = client.session.declare_subscriber(
        f"{client.prefix}/recorded_data",
        client._handle_recorded_data,
    )
    client.status_sub = client.session.declare_subscriber(
        f"{client.prefix}/daemon_status",
        client._handle_status,
    )
    client.task_request_pub = client.session.declare_publisher(f"{client.prefix}/task")
    client.task_progress_sub = client.session.declare_subscriber(
        f"{client.prefix}/task_progress",
        client._handle_task_progress,
    )

    # 创建 ReachyMini 实例并替换客户端
    mini = ReachyMini.__new__(ReachyMini)
    mini.robot_name = "reachy_mini"
    mini.client = client
    mini._last_head_pose = None
    mini.is_recording = False

    mini.T_head_cam = np.eye(4)
    mini.T_head_cam[:3, 3][:] = [0.0437, 0, 0.0512]
    mini.T_head_cam[:3, :3] = np.array(
        [
            [0, 0, 1],
            [-1, 0, 0],
            [0, -1, 0],
        ]
    )

    mini.media_manager = MediaManager(
        use_sim=client.get_status()["simulation_enabled"],
        backend=MediaBackend.NO_MEDIA,
        log_level="INFO",
        signalling_host=client.get_status()["wlan_ip"],
    )

    client.wait_for_connection()
    mini.set_automatic_body_yaw(True)

    try:
        t0 = time.time()

        root = tk.Tk()
        root.title("Set Head Euler Angles")

        roll_var = tk.DoubleVar(value=0.0)
        pitch_var = tk.DoubleVar(value=0.0)
        yaw_var = tk.DoubleVar(value=0.0)

        tk.Label(root, text="Roll (deg):").grid(row=0, column=0)
        tk.Scale(
            root, variable=roll_var, from_=-45, to=45, orient=tk.HORIZONTAL, length=200
        ).grid(row=0, column=1)
        tk.Label(root, text="Pitch (deg):").grid(row=1, column=0)
        tk.Scale(
            root, variable=pitch_var, from_=-45, to=45, orient=tk.HORIZONTAL, length=200
        ).grid(row=1, column=1)
        tk.Label(root, text="Yaw (deg):").grid(row=2, column=0)
        tk.Scale(
            root, variable=yaw_var, from_=-175, to=175, orient=tk.HORIZONTAL, length=200
        ).grid(row=2, column=1)

        # Add sliders for X, Y, Z position
        x_var = tk.DoubleVar(value=0.0)
        y_var = tk.DoubleVar(value=0.0)
        z_var = tk.DoubleVar(value=0.0)

        tk.Label(root, text="X (m):").grid(row=3, column=0)
        tk.Scale(
            root,
            variable=x_var,
            from_=-0.05,
            to=0.05,
            resolution=0.001,
            orient=tk.HORIZONTAL,
            length=200,
        ).grid(row=3, column=1)
        tk.Label(root, text="Y (m):").grid(row=4, column=0)
        tk.Scale(
            root,
            variable=y_var,
            from_=-0.05,
            to=0.05,
            resolution=0.001,
            orient=tk.HORIZONTAL,
            length=200,
        ).grid(row=4, column=1)
        tk.Label(root, text="Z (m):").grid(row=5, column=0)
        tk.Scale(
            root,
            variable=z_var,
            from_=-0.05,
            to=0.03,
            resolution=0.001,
            orient=tk.HORIZONTAL,
            length=200,
        ).grid(row=5, column=1)

        tk.Label(root, text="Body Yaw (deg):").grid(row=6, column=0)
        body_yaw_var = tk.DoubleVar(value=0.0)
        tk.Scale(
            root,
            variable=body_yaw_var,
            from_=-180,
            to=180,
            resolution=1.0,
            orient=tk.HORIZONTAL,
            length=200,
        ).grid(row=6, column=1)

        mini.goto_target(create_head_pose(), antennas=[0.0, 0.0], duration=1.0)

        # Run the GUI in a non-blocking way
        root.update()

        try:
            while True:
                t = time.time() - t0
                target = np.deg2rad(30) * np.sin(2 * np.pi * 0.5 * t)

                head = np.eye(4)
                head[:3, 3] = [0, 0, 0.0]

                # Read values from the GUI
                roll = np.deg2rad(roll_var.get())
                pitch = np.deg2rad(pitch_var.get())
                yaw = np.deg2rad(yaw_var.get())
                head[:3, :3] = R.from_euler(
                    "xyz", [roll, pitch, yaw], degrees=False
                ).as_matrix()
                head[:3, 3] = [x_var.get(), y_var.get(), z_var.get()]

                root.update()

                mini.set_target(
                    head=head,
                    body_yaw=np.deg2rad(body_yaw_var.get()),
                    antennas=np.array([target, -target]),
                )
        except KeyboardInterrupt:
            pass
        finally:
            try:
                root.destroy()
            except:
                pass
            mini.media_manager.close()
            mini.client.disconnect()
    except Exception as e:
        print(f"Error: {e}")
        mini.media_manager.close()
        mini.client.disconnect()
        raise


if __name__ == "__main__":
    main()
