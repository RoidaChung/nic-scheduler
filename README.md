# NIC-Scheduler

**網路卡排程管理工具 - 輕鬆排程網路卡的啟用與禁用時間**


## 中文

NIC-Scheduler 是一個網路卡排程管理工具，讓您可以輕鬆設定網路卡的啟用與禁用時間，無論是單次排程還是週期性排程，都能滿足您的需求。

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


---


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


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
