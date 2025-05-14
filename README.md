
```markdown
<div align="center">
  <img src="screenshots/nic-scheduler-logo.png" alt="NIC-Scheduler Logo" width="200"/>
  <h1>NIC-Scheduler</h1>
  <p><strong>網路卡排程管理工具 - 輕鬆排程網路卡的啟用與禁用時間</strong></p>
  <p>
    <a href="#features">功能特色</a> |
    <a href="#quick-start">快速開始</a> |
    <a href="#documentation">文檔</a> |
    <a href="#contributing">貢獻</a> |
    <a href="#license">授權</a>
  </p>
  <p>
    <a href="#english">English</a> |
    <a href="#chinese">中文</a>
  </p>
</div>

<a name="chinese"></a>
## 中文

NIC-Scheduler 是一個強大的網路卡排程管理工具，讓您可以輕鬆設定網路卡的啟用與禁用時間，無論是單次排程還是週期性排程，都能滿足您的需求。

### 功能特色

- **單次排程**：設定特定日期的網路卡啟用/禁用時間
- **週期性排程**：按週幾設定重複的網路卡啟用/禁用時間
- **使用者管理**：支援多使用者登入，包含管理員與一般使用者權限
- **日誌系統**：詳細記錄所有操作與排程執行情況

### 快速開始

1. 克隆儲存庫並安裝依賴
   ```bash
   git clone https://github.com/RoidaChung/nic-scheduler.git
   cd nic-scheduler
   pip install -r requirements.txt
   ```

2. 運行程式
   ```bash
   python nic-scheduler.py
   ```

3. 預設登入
   - 使用者名稱：admin
   - 密碼：admin123

### 文檔與支援

- [使用手冊](docs/user-guide.zh-TW.md)
- [安裝指南](docs/installation.zh-TW.md)
- [常見問題](docs/faq.md)

---

<a name="english"></a>
## English

NIC-Scheduler is a powerful Network Interface Card scheduling tool that allows you to easily set enable and disable times for your network cards, whether for one-time schedules or recurring patterns.

### Features

- **Single Schedule**: Set specific dates for NIC enable/disable times
- **Recurring Schedule**: Set weekly patterns for NIC enable/disable times
- **User Management**: Support for multiple users with admin and regular user privileges
- **Logging System**: Detailed logs of all operations and schedule executions

### Quick Start

1. Clone repository and install dependencies
   ```bash
   git clone https://github.com/RoidaChung/nic-scheduler.git
   cd nic-scheduler
   pip install -r requirements.txt
   ```

2. Run the application
   ```bash
   python nic-scheduler.py
   ```

3. Default login
   - Username: admin
   - Password: admin123

### Documentation & Support

- [User Guide](docs/user-guide.en.md)
- [Installation Guide](docs/installation.en.md)
- [FAQ](docs/faq.md)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### 3. 創建文檔文件內容

#### docs/user-guide.zh-TW.md
```markdown
# NIC-Scheduler 使用手冊

## 登入系統
- 預設管理員：admin / admin123
- 首次登入後請立即修改密碼

## 單次排程
1. 選擇網路卡
2. 設定日期 (YYYY/MM/DD)
3. 設定連接與斷開時間
4. 點擊「Add to List」

## 週期性排程
1. 選擇網路卡
2. 勾選需要排程的星期幾
3. 設定連接與斷開時間
4. 點擊「Add Recurring Schedule」

## 管理功能
- 刪除排程：選中排程後點擊「Delete Selected」
- 測試網路卡：點擊「Test NIC Operations」
- 查看日誌：切換到「Logs」頁籤
- 管理使用者：管理員可在「Administration」頁籤管理使用者
```

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
```

