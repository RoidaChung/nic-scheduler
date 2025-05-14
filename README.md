# GitHub 專案雙語指南：NIC-Scheduler (精簡版)

## 1. 雙語 README.md

```markdown
# NIC-Scheduler

[English](#english) | [中文](#chinese)

<a name="chinese"></a>
## 中文

網路卡排程管理工具 - 輕鬆排程網路卡的啟用與禁用時間

### 功能特色
- 單次排程：設定特定日期的網路卡啟用/禁用時間
- 週期性排程：按週幾設定重複的網路卡啟用/禁用時間
- 使用者管理：支援多使用者登入，包含管理員與一般使用者權限
- 日誌系統：詳細記錄所有操作與排程執行情況

### 快速開始
1. 克隆儲存庫並安裝依賴
   ```bash
   git clone https://github.com/RoidaChung/nic-scheduler.git
   cd nic-scheduler
   pip install -r requirements.txt
   ```
2. 運行程式：`python nic-scheduler.py`
3. 預設登入：admin / admin123

### 文檔與支援
- [使用手冊](docs/user-guide.zh-TW.md)
- [安裝指南](docs/installation.zh-TW.md)

---

<a name="english"></a>
## English

Network Interface Card Scheduler - Easily schedule the enabling and disabling of your network cards

### Features
- Single Schedule: Set specific dates for NIC enable/disable times
- Recurring Schedule: Set weekly patterns for NIC enable/disable times
- User Management: Support for multiple users with admin and regular user privileges
- Logging System: Detailed logs of all operations and schedule executions

### Quick Start
1. Clone repository and install dependencies
   ```bash
   git clone https://github.com/RoidaChung/nic-scheduler.git
   cd nic-scheduler
   pip install -r requirements.txt
   ```
2. Run the application: `python nic-scheduler.py`
3. Default login: admin / admin123

### Documentation & Support
- [User Guide](docs/user-guide.en.md)
- [Installation Guide](docs/installation.en.md)
```

## 2. 中文使用手冊 (docs/user-guide.zh-TW.md)

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

## 3. 英文使用手冊 (docs/user-guide.en.md)

```markdown
# NIC-Scheduler User Guide

## Login System
- Default admin: admin / admin123
- Change password after first login

## Single Schedule
1. Select network card
2. Set date (YYYY/MM/DD)
3. Set connect and disconnect times
4. Click "Add to List"

## Recurring Schedule
1. Select network card
2. Check days of week for scheduling
3. Set connect and disconnect times
4. Click "Add Recurring Schedule"

## Management Functions
- Delete schedules: Select schedule and click "Delete Selected"
- Test network card: Click "Test NIC Operations"
- View logs: Switch to "Logs" tab
- Manage users: Admins can manage users in "Administration" tab
```

## 4. 雙語議題模板 (.github/ISSUE_TEMPLATE/bug_report.md)

```markdown
---
name: 錯誤報告 | Bug Report
about: 創建一個錯誤報告以幫助我們改進 | Create a bug report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

<!-- 請用中文或英文填寫 | Please fill in Chinese or English -->

**描述錯誤 | Describe the bug**
清晰簡潔地描述錯誤是什麼。
A clear and concise description of what the bug is.

**重現步驟 | Steps to Reproduce**
1. 前往 '...' | Go to '...'
2. 點擊 '....' | Click on '....'
3. 查看錯誤 | See error

**預期行為 | Expected behavior**
描述您期望發生的情況。
Describe what you expected to happen.

**環境信息 | Environment**
 - 操作系統 | OS: [例如 | e.g. Windows 10]
 - Python 版本 | Version: [例如 | e.g. 3.9.5]
```

## 5. 雙語常見問題 (docs/faq.md)

```markdown
# NIC-Scheduler 常見問題 | Frequently Asked Questions

[中文](#chinese) | [English](#english)

<a name="chinese"></a>
## 中文

### Q: 為什麼我需要 NIC-Scheduler？
A: 當您需要在特定時間自動控制網路連接時，例如工作時間自動啟用公司網路，或在夜間自動禁用網路以節省電力。

### Q: 如何確保排程在電腦重啟後仍然有效？
A: 將程式設置為開機自動啟動，或使用系統的排程工具來啟動程式。

### Q: 忘記密碼怎麼辦？
A: 刪除 `nic_users.json` 檔案，程式將在下次啟動時重新創建預設管理員帳戶。

---

<a name="english"></a>
## English

### Q: Why do I need NIC-Scheduler?
A: When you need to automatically control network connections at specific times, such as enabling company network during work hours or disabling network at night to save power.

### Q: How can I ensure schedules remain effective after computer restart?
A: Set the program to start automatically at boot, or use system scheduling tools to start the program.

### Q: What if I forget my password?
A: Delete the `nic_users.json` file, and the program will recreate the default administrator account the next time it starts.
```

## 6. 專案目錄結構

```
nic-scheduler/
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── docs/
│   ├── user-guide.en.md
│   ├── user-guide.zh-TW.md
│   ├── installation.en.md
│   ├── installation.zh-TW.md
│   └── faq.md
├── screenshots/
│   ├── main-interface.png
│   └── recurring-schedule.png
├── .gitignore
├── LICENSE
├── README.md
├── nic-scheduler.py
└── requirements.txt
```

## 7. 雙語發布說明 (Release Notes)

```markdown
# NIC-Scheduler v1.0.0

[中文](#chinese) | [English](#english)

<a name="chinese"></a>
## 中文

### 新功能
- 單次排程：設定特定日期的網路卡啟用/禁用時間
- 週期性排程：按週幾設定重複的網路卡啟用/禁用時間
- 使用者管理：支援多使用者登入
- 日誌系統：詳細記錄所有操作

### 安裝方法
1. 下載 ZIP 檔案或使用 git clone
2. 安裝依賴：`pip install -r requirements.txt`
3. 運行程式：`python nic-scheduler.py`

---

<a name="english"></a>
## English

### New Features
- Single Schedule: Set specific dates for NIC enable/disable times
- Recurring Schedule: Set weekly patterns for NIC enable/disable times
- User Management: Support for multiple users
- Logging System: Detailed logs of all operations

### Installation
1. Download ZIP file or use git clone
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python nic-scheduler.py`
```

## 8. 雙語故障排除指南 (docs/troubleshooting.md)

```markdown
# 故障排除指南 | Troubleshooting Guide

[中文](#chinese) | [English](#english)

<a name="chinese"></a>
## 中文

### 啟動問題
- **程式無法啟動**
  - 確認已安裝 Python 3.6+
  - 運行 `pip install -r requirements.txt`
  - 以管理員身份運行

### 網路卡操作問題
- **無法控制網路卡**
  - 確保以管理員權限運行程式
  - 使用「Test NIC Operations」按鈕測試
  - Windows 需要 PowerShell 5.0+

---

<a name="english"></a>
## English

### Startup Issues
- **Program fails to start**
  - Confirm Python 3.6+ is installed
  - Run `pip install -r requirements.txt`
  - Run as administrator

### Network Card Operation Issues
- **Cannot control network cards**
  - Ensure program runs with administrator privileges
  - Use "Test NIC Operations" button to test
  - Windows requires PowerShell 5.0+
```
