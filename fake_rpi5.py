from pymavlink import mavutil
import time
import threading
import math

# 目標：Windows Bridge 監聽的 port
TARGET_IP = "127.0.0.1"
TARGET_PORT = 14540

print(f"🤖 假 RPI5 啟動！(使用 pymavlink) 發送至 {TARGET_IP}:{TARGET_PORT}")
print("指令: [a] ARM  [t] TAKEOFF  [l] LAND  [auto] 自動起飛  [q] 離開\n")

# 建立 UDP 連線 (udpout 代表我們是主動發送端)
master = mavutil.mavlink_connection(
    f'udpout:{TARGET_IP}:{TARGET_PORT}', 
    source_system=255, 
    source_component=190
)

def heartbeat_loop():
    """背景持續送心跳 (極度重要，否則 PX4 會拒絕指令或自動上鎖)"""
    while True:
        master.mav.heartbeat_send(
            mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER,
            mavutil.mavlink.MAV_AUTOPILOT_INVALID,
            0, 0, 0
        )
        time.sleep(1)

# 啟動背景心跳執行緒
threading.Thread(target=heartbeat_loop, daemon=True).start()

while True:
    cmd = input(">>> ").strip().lower()
    
    if cmd == 'q':
        print("關閉程式...")
        break
        
    elif cmd == 'a':
        # MAV_CMD_COMPONENT_ARM_DISARM (400), Param1 = 1 (ARM)
        master.mav.command_long_send(
            1, 1, # Target System, Target Component (PX4 預設為 1, 1)
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 1, 0, 0, 0, 0, 0, 0
        )
        print("✌️  發送單獨 ARM 指令 (注意：超時未動作會自動上鎖)")
        
    elif cmd == 't':
        # MAV_CMD_NAV_TAKEOFF (22)
        # 關鍵修正：Param 4(Yaw), 5(Lat), 6(Lon) 設為 math.nan 代表維持當前座標 (原地起飛)
        master.mav.command_long_send(
            1, 1,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0, 0, 0, 0, math.nan, math.nan, math.nan, 5.0 
        )
        print("✋  發送單獨 TAKEOFF 指令 (原地起飛，高度 5m)")
        
    elif cmd == 'l':
        # MAV_CMD_NAV_LAND (21)
        # 同樣使用 math.nan 讓它在當前位置原地降落
        master.mav.command_long_send(
            1, 1,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0, 0, 0, 0, math.nan, math.nan, math.nan, 0
        )
        print("✊  發送 LAND 指令 (原地降落)")
        
    elif cmd == 'auto':
        print("🚀 [自動流程] 1. 發送 ARM 指令...")
        master.mav.command_long_send(
            1, 1, 
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 
            0, 1, 0, 0, 0, 0, 0, 0
        )
        
        # 給 Gazebo 馬達 2 秒鐘的物理加速時間 (怠速)，避免超時
        print("⏳ 螺旋槳預熱中 (等待 2 秒)...")
        time.sleep(2) 
        
        print("🛫 [自動流程] 2. 發送 TAKEOFF 指令 (原地起飛，目標高度 5m)...")
        master.mav.command_long_send(
            1, 1, 
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 
            0, 0, 0, 0, math.nan, math.nan, math.nan, 5.0 
        )
        
    else:
        print("未知指令，請輸入 a / t / l / auto / q")