#### docs/installation.zh-TW.md
```markdown
# NIC-Scheduler 安裝指南

## 系統需求
- Python 3.6 或更高版本
- Windows 7/10/11 或 Linux/macOS

## 安裝步驟

### Windows
1. 安裝 Python (如果尚未安裝)
   - 從 [Python 官網](https://www.python.org/downloads/) 下載並安裝
   - 安裝時勾選「Add Python to PATH」

2. 下載 NIC-Scheduler
   ```
   git clone https://github.com/RoidaChung/nic-scheduler.git
   cd nic-scheduler
   ```

3. 安裝依賴
   ```
   pip install -r requirements.txt
   ```

4. 運行程式
   ```
   python nic-scheduler.py
   ```

### Linux/macOS
1. 安裝 Python (如果尚未安裝)
   ```
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip

   # macOS
   brew install python
   ```

2. 下載 NIC-Scheduler
   ```
   git clone https://github.com/RoidaChung/nic-scheduler.git
   cd nic-scheduler
   ```

3. 安裝依賴
   ```
   pip3 install -r requirements.txt
   ```

4. 運行程式
   ```
   python3 nic-scheduler.py
   ```

## 設置為開機啟動

### Windows
1. 創建批處理檔案 `start_nic_scheduler.bat`
   ```
   @echo off
   cd 路徑\到\nic-scheduler
   python nic-scheduler.py
   ```

2. 將批處理檔案的捷徑放入啟動資料夾
   - 按 Win+R，輸入 `shell:startup`，然後將捷徑放入開啟的資料夾

### Linux
1. 創建服務檔案
   ```
   sudo nano /etc/systemd/system/nic-scheduler.service
   ```

2. 添加以下內容
   ```
   [Unit]
   Description=NIC Scheduler Service
   After=network.target

   [Service]
   User=YOUR_USERNAME
   WorkingDirectory=/path/to/nic-scheduler
   ExecStart=/usr/bin/python3 /path/to/nic-scheduler/nic-scheduler.py
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

3. 啟用服務
   ```
   sudo systemctl enable nic-scheduler.service
   sudo systemctl start nic-scheduler.service
   ```