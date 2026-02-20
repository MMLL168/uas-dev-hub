import socket
import threading
import time
import subprocess
import re
import struct  # 新增：用於解碼二進制數據

# === 設定 ===
EXTERNAL_PORT = 14540 
WSL_PORT = 14580

# === MAVLink 指令對照表 ===
MAV_CMD = {
    22: "🚁 起飛 (TAKEOFF)",
    21: "🛬 降落 (LAND)",
    400: "🔓 解鎖/上鎖 (ARM/DISARM)",
    511: "ℹ️ 設定模式 (SET_MODE)"
}

def get_wsl_ip():
    """自動偵測 WSL 的 IP 地址"""
    try:
        # 嘗試 wsl hostname -I (最準確)
        wsl_ip = subprocess.check_output(["wsl", "hostname", "-I"]).decode().strip().split(' ')[0]
        return wsl_ip
    except:
        try:
            # 備用方案: ipconfig (較不穩)
            result = subprocess.check_output("ipconfig", shell=True).decode('big5', errors='ignore')
            ips = re.findall(r"IPv4 位址[ .]+: (172\.[0-9]+\.[0-9]+\.[0-9]+)", result)
            return ips[0] if ips else input("請手動輸入 WSL IP: ")
        except:
            return input("請手動輸入 WSL IP: ")

def parse_mavlink_packet(data):
    """解析 MAVLink v1 封包並回傳可讀訊息"""
    try:
        if len(data) < 6: return None
        
        # MAVLink v1 Header 結構
        # [0]=Magic(0xFE), [1]=Len, [2]=Seq, [3]=Sys, [4]=Comp, [5]=MsgID
        magic = data[0]
        msg_id = data[5]

        # 1. 心跳包 (Msg ID 0)
        if msg_id == 0:
            return "💓 心跳包 (HEARTBEAT)"

        # 2. COMMAND_LONG (Msg ID 76) - 這是最重要的指令包
        elif msg_id == 76:
            # 在 MAVLink v1 wire format 中，COMMAND_LONG 的 Payload 排列如下：
            # param1~7 (4bytes*7) | command (2bytes) | target_sys | target_comp | confirm
            # Payload 從 index 6 開始
            # Command ID 在 Payload 的第 28 bytes 處 (7個 float 之後)
            # 所以絕對位置是 6 + 28 = 34
            if len(data) >= 36:
                cmd_id = struct.unpack('<H', data[34:36])[0] # Little-endian unsigned short
                cmd_name = MAV_CMD.get(cmd_id, f"未知指令 ({cmd_id})")
                
                # 如果是解鎖指令 (400)，我們可以進一步看 param1
                if cmd_id == 400:
                    param1 = struct.unpack('<f', data[6:10])[0]
                    action = "解鎖" if param1 == 1.0 else "上鎖"
                    return f"🔓 {action} (ARM/DISARM)"
                
                return f"⚡ {cmd_name}"
            
        return f"📦 其他封包 (ID: {msg_id})"

    except Exception as e:
        return f"解析錯誤: {e}"

def bridge():
    wsl_ip = get_wsl_ip()
    print("="*50)
    print(f"🚁 MAVLink 智慧橋接器 (Smart Bridge)")
    print(f"外部來源 (RPi5): 0.0.0.0:{EXTERNAL_PORT}")
    print(f"內部目標 (WSL) : {wsl_ip}:{WSL_PORT}")
    print("="*50)

    sock_ext = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_ext.bind(('0.0.0.0', EXTERNAL_PORT))
    
    sock_int = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rpi_client_addr = None

    print(f"✅ 正在監聽並即時解碼指令...")
    print(f"⚠️  請確保 Windows 防火牆允許 Python 通過！")

    def forward_to_wsl():
        nonlocal rpi_client_addr
        while True:
            try:
                data, addr = sock_ext.recvfrom(4096)
                
                # --- 即時解碼顯示 ---
                # 只顯示非心跳包，或者每 5 秒顯示一次心跳以免洗版
                # 這裡設定：只要是 Command (ID 76) 就一定顯示
                if len(data) > 0:
                    msg = parse_mavlink_packet(data)
                    
                    # 過濾掉心跳包顯示，讓畫面乾淨，只專注看動作指令
                    if msg and "心跳" not in msg:
                        print(f"[{time.strftime('%H:%M:%S')}] 🔥 {msg} | 來自: {addr[0]}")
                    
                    # 如果你想看心跳包確認連線，可以把下面這行註解打開
                    # elif msg and "心跳" in msg: print(".", end="", flush=True)
                # -------------------

                if rpi_client_addr != addr:
                    print(f"\n[連線] RPi5 已連接: {addr}")
                    rpi_client_addr = addr
                
                sock_int.sendto(data, (wsl_ip, WSL_PORT))
            except Exception as e:
                print(f"轉發錯誤: {e}")

    t1 = threading.Thread(target=forward_to_wsl)
    t1.daemon = True
    t1.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n橋接器已關閉")

if __name__ == "__main__":
    bridge()