import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import datetime
import schedule
import time
import threading
import json
import os
import logging
import hashlib
import calendar
from datetime import datetime, timedelta

class NICScheduler:
    def __init__(self):
        # 設置日誌
        self.setup_logging()
        logging.info("NIC Scheduler started")
        
        # 使用者認證
        self.users = {}
        self.current_user = None
        self.user_file = "nic_users.json"
        self.load_users()
        
        # 登入檢查
        if not self.login():
            logging.warning("Login failed or cancelled. Exiting application.")
            exit()
        
        # 初始化主視窗
        self.root = tk.Tk()
        self.root.title(f"NIC Custom Date Scheduler - Logged in as: {self.current_user}")
        self.root.geometry("620x520")  # 增加視窗大小以容納新功能
        
        # 儲存排程
        self.schedules = []
        self.schedule_file = "nic_schedules.json"
        self.adapter_details = []  # 儲存網路卡詳細資訊
        self.load_schedules()
        
        # 建立界面
        self.create_ui()
        
        # 啟動排程執行緒
        self.stop_thread = False
        self.scheduler_thread = threading.Thread(target=self.run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        # 設置定期日誌檢查
        self.log_check_thread = threading.Thread(target=self.periodic_log_check)
        self.log_check_thread.daemon = True
        self.log_check_thread.start()
    
    def setup_logging(self):
        """設置日誌系統"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f"nic_scheduler_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 同時輸出到控制台
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
    
    def load_users(self):
        """載入使用者資訊"""
        try:
            if os.path.exists(self.user_file):
                with open(self.user_file, 'r') as f:
                    self.users = json.load(f)
            else:
                # 創建預設管理員帳戶
                admin_password = "admin123"  # 預設密碼
                hashed_password = hashlib.sha256(admin_password.encode()).hexdigest()
                self.users = {
                    "admin": {
                        "password": hashed_password,
                        "role": "admin"
                    }
                }
                self.save_users()
                logging.info("Created default admin account")
        except Exception as e:
            logging.error(f"Failed to load users: {e}")
            self.users = {}
    
    def save_users(self):
        """保存使用者資訊"""
        try:
            with open(self.user_file, 'w') as f:
                json.dump(self.users, f)
        except Exception as e:
            logging.error(f"Failed to save users: {e}")
            messagebox.showerror("Error", f"Failed to save user information: {e}")
    
    def login(self):
        """使用者登入視窗"""
        login_window = tk.Tk()
        login_window.title("NIC Scheduler Login")
        login_window.geometry("300x200")
        login_window.resizable(False, False)
        
        # 置中顯示
        screen_width = login_window.winfo_screenwidth()
        screen_height = login_window.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 200) // 2
        login_window.geometry(f"300x200+{x}+{y}")
        
        # 標題
        tk.Label(login_window, text="NIC Scheduler Login", font=("Arial", 14, "bold")).pack(pady=10)
        
        # 使用者名稱
        tk.Label(login_window, text="Username:").pack(pady=5)
        username_entry = tk.Entry(login_window, width=20)
        username_entry.pack(pady=5)
        
        # 密碼
        tk.Label(login_window, text="Password:").pack(pady=5)
        password_entry = tk.Entry(login_window, width=20, show="*")
        password_entry.pack(pady=5)
        
        # 登入狀態
        login_status = {"success": False}
        
        def do_login():
            username = username_entry.get()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Username and password are required")
                return
            
            # 驗證使用者
            if username in self.users:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if self.users[username]["password"] == hashed_password:
                    self.current_user = username
                    login_status["success"] = True
                    logging.info(f"User {username} logged in successfully")
                    login_window.destroy()
                else:
                    messagebox.showerror("Error", "Invalid password")
                    logging.warning(f"Failed login attempt for user {username}")
            else:
                messagebox.showerror("Error", "User not found")
                logging.warning(f"Login attempt with non-existent user: {username}")
        
        # 登入按鈕
        login_button = tk.Button(login_window, text="Login", command=do_login)
        login_button.pack(pady=10)
        
        # 註冊新使用者按鈕
        register_button = tk.Button(login_window, text="Register New User", 
                                   command=lambda: self.register_new_user(login_window))
        register_button.pack(pady=5)
        
        login_window.mainloop()
        
        return login_status["success"]
    
    def register_new_user(self, parent_window):
        """註冊新使用者"""
        # 檢查是否有管理員權限
        if self.current_user and self.users.get(self.current_user, {}).get("role") != "admin":
            messagebox.showerror("Error", "Only administrators can register new users")
            return
            
        register_window = tk.Toplevel(parent_window)
        register_window.title("Register New User")
        register_window.geometry("300x200")
        register_window.resizable(False, False)
        
        # 置中顯示
        screen_width = parent_window.winfo_screenwidth()
        screen_height = parent_window.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 200) // 2
        register_window.geometry(f"300x200+{x}+{y}")
        
        # 標題
        tk.Label(register_window, text="Register New User", font=("Arial", 14, "bold")).pack(pady=10)
        
        # 使用者名稱
        tk.Label(register_window, text="Username:").pack(pady=5)
        username_entry = tk.Entry(register_window, width=20)
        username_entry.pack(pady=5)
        
        # 密碼
        tk.Label(register_window, text="Password:").pack(pady=5)
        password_entry = tk.Entry(register_window, width=20, show="*")
        password_entry.pack(pady=5)
        
        # 角色選擇
        role_var = tk.StringVar(value="user")
        role_frame = tk.Frame(register_window)
        role_frame.pack(pady=5)
        tk.Radiobutton(role_frame, text="User", variable=role_var, value="user").pack(side=tk.LEFT)
        tk.Radiobutton(role_frame, text="Admin", variable=role_var, value="admin").pack(side=tk.LEFT)
        
        def do_register():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Username and password are required")
                return
                
            if username in self.users:
                messagebox.showerror("Error", "Username already exists")
                return
                
            # 添加新使用者
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.users[username] = {
                "password": hashed_password,
                "role": role
            }
            self.save_users()
            
            messagebox.showinfo("Success", f"User {username} registered successfully")
            logging.info(f"New user registered: {username}, role: {role}")
            register_window.destroy()
        
        # 註冊按鈕
        register_button = tk.Button(register_window, text="Register", command=do_register)
        register_button.pack(pady=10)
    
    def create_ui(self):
        """建立使用者界面"""
        # 建立頁籤控件
        self.tab_control = ttk.Notebook(self.root)
        
        # 建立頁籤
        self.tab_single = ttk.Frame(self.tab_control)
        self.tab_recurring = ttk.Frame(self.tab_control)
        self.tab_logs = ttk.Frame(self.tab_control)
        self.tab_admin = ttk.Frame(self.tab_control)
        self.tab_about = ttk.Frame(self.tab_control)  # 新增 about 頁籤
        
        # 添加頁籤
        self.tab_control.add(self.tab_single, text='Single Schedule')
        self.tab_control.add(self.tab_recurring, text='Recurring Schedule')
        self.tab_control.add(self.tab_logs, text='Logs')
        
        # 如果是管理員，添加管理頁籤
        if self.users.get(self.current_user, {}).get("role") == "admin":
            self.tab_control.add(self.tab_admin, text='Administration')
        
        # 添加關於頁籤
        self.tab_control.add(self.tab_about, text='About')
        
        self.tab_control.pack(expand=1, fill="both")
        
        # 建立單次排程頁籤內容
        self.create_single_schedule_tab()
        
        # 建立週期性排程頁籤內容
        self.create_recurring_schedule_tab()
        
        # 建立日誌頁籤內容
        self.create_logs_tab()
        
        # 如果是管理員，建立管理頁籤內容
        if self.users.get(self.current_user, {}).get("role") == "admin":
            self.create_admin_tab()
        
        # 建立關於本程式頁籤內容
        self.create_about_tab()

        # 顯示狀態標籤
        self.status_label = tk.Label(self.root, text="Ready. Next check: -")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

    def create_about_tab(self):
        """建立關於本程式頁籤內容"""
        # 中央區域框架
        about_frame = tk.Frame(self.tab_about, padx=20, pady=20)
        about_frame.pack(expand=True, fill="both")
        
        # 程式標題
        title_label = tk.Label(about_frame, text="NIC Custom Date Scheduler", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 作者資訊
        author_label = tk.Label(about_frame, text="作者: Roida Chung", font=("Arial", 12))
        author_label.pack(pady=5)
        
        # GitHub 網址
        github_url = "https://github.com/RoidaChung/nic-scheduler"
        github_label = tk.Label(about_frame, text=f"GitHub: {github_url}", font=("Arial", 12))
        github_label.pack(pady=5)
        
        # 版本資訊
        version_label = tk.Label(about_frame, text="版本: 1.0.0", font=("Arial", 12))
        version_label.pack(pady=5)
        
        # 描述
        description = "這是一個用於排程網路卡啟用/禁用的工具，支援單次排程和週期性排程。"
        desc_label = tk.Label(about_frame, text=description, font=("Arial", 11), wraplength=400)
        desc_label.pack(pady=10)

    def create_single_schedule_tab(self):
        """建立單次排程頁籤內容"""
        # NIC 選擇
        tk.Label(self.tab_single, text="Select NIC:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.nic_combo = ttk.Combobox(self.tab_single, width=30)
        self.nic_combo.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        self.get_nics()
        
        # 日期選擇
        tk.Label(self.tab_single, text="Date:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.date_entry = tk.Entry(self.tab_single, width=15)
        self.date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.date_entry.insert(0, datetime.now().strftime("%Y/%m/%d"))
        
        # 連接時間
        tk.Label(self.tab_single, text="Connect Time:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        time_frame = tk.Frame(self.tab_single)
        time_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        self.connect_hour = ttk.Combobox(time_frame, width=5, values=[f"{i:02d}" for i in range(24)])
        self.connect_hour.pack(side=tk.LEFT)
        self.connect_hour.current(8)  # 預設 08:00
        
        tk.Label(time_frame, text=":").pack(side=tk.LEFT)
        
        self.connect_minute = ttk.Combobox(time_frame, width=5, values=[f"{i:02d}" for i in range(0, 60, 5)])
        self.connect_minute.pack(side=tk.LEFT)
        self.connect_minute.current(0)  # 預設 00 分
        
        # 斷開時間
        tk.Label(self.tab_single, text="Disconnect Time:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        time_frame2 = tk.Frame(self.tab_single)
        time_frame2.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        self.disconnect_hour = ttk.Combobox(time_frame2, width=5, values=[f"{i:02d}" for i in range(24)])
        self.disconnect_hour.pack(side=tk.LEFT)
        self.disconnect_hour.current(17)  # 預設 17:00
        
        tk.Label(time_frame2, text=":").pack(side=tk.LEFT)
        
        self.disconnect_minute = ttk.Combobox(time_frame2, width=5, values=[f"{i:02d}" for i in range(0, 60, 5)])
        self.disconnect_minute.pack(side=tk.LEFT)
        self.disconnect_minute.current(0)  # 預設 00 分
        
        # 加入排程按鈕
        add_button = tk.Button(self.tab_single, text="Add to List", command=self.add_to_list)
        add_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        # 排程列表
        list_frame = tk.Frame(self.tab_single)
        list_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        self.schedule_tree = ttk.Treeview(list_frame, columns=("Date", "Connect", "Disconnect", "NIC", "Type"), show="headings")
        self.schedule_tree.heading("Date", text="Date")
        self.schedule_tree.heading("Connect", text="Connect Time")
        self.schedule_tree.heading("Disconnect", text="Disconnect Time")
        self.schedule_tree.heading("NIC", text="Network Card")
        self.schedule_tree.heading("Type", text="Schedule Type")
        self.schedule_tree.column("Date", width=80)
        self.schedule_tree.column("Connect", width=80)
        self.schedule_tree.column("Disconnect", width=80)
        self.schedule_tree.column("NIC", width=240)
        self.schedule_tree.column("Type", width=80)
        self.schedule_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加滾動條
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.schedule_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.schedule_tree.configure(yscrollcommand=scrollbar.set)
        
        # 按鈕區域
        button_frame = tk.Frame(self.tab_single)
        button_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        
        # 刪除排程按鈕
        delete_button = tk.Button(button_frame, text="Delete Selected", command=self.delete_selected)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # 儲存排程按鈕
        save_button = tk.Button(button_frame, text="Save Schedules", command=self.save_schedules)
        save_button.pack(side=tk.LEFT, padx=5)
        
        # 測試網路卡按鈕
        test_button = tk.Button(button_frame, text="Test NIC Operations", command=self.test_nic_operations)
        test_button.pack(side=tk.LEFT, padx=5)
        
        # 載入已有排程到表格
        self.refresh_schedule_list()
    
    def create_recurring_schedule_tab(self):
        """建立週期性排程頁籤內容"""
        # NIC 選擇
        tk.Label(self.tab_recurring, text="Select NIC:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.recurring_nic_combo = ttk.Combobox(self.tab_recurring, width=30)
        self.recurring_nic_combo.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        self.recurring_nic_combo['values'] = self.nic_combo['values']
        if self.nic_combo.current() >= 0:
            self.recurring_nic_combo.current(self.nic_combo.current())
        
        # 週期選擇
        tk.Label(self.tab_recurring, text="Schedule on:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        days_frame = tk.Frame(self.tab_recurring)
        days_frame.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        
        # 建立星期選擇核取方塊
        self.day_vars = []
        for i, day in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
            var = tk.BooleanVar(value=True if i < 5 else False)  # 預設選擇週一至週五
            self.day_vars.append(var)
            tk.Checkbutton(days_frame, text=day[:3], variable=var).pack(side=tk.LEFT)
        
        # 連接時間
        tk.Label(self.tab_recurring, text="Connect Time:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        time_frame = tk.Frame(self.tab_recurring)
        time_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        self.recurring_connect_hour = ttk.Combobox(time_frame, width=5, values=[f"{i:02d}" for i in range(24)])
        self.recurring_connect_hour.pack(side=tk.LEFT)
        self.recurring_connect_hour.current(8)  # 預設 08:00
        
        tk.Label(time_frame, text=":").pack(side=tk.LEFT)
        
        self.recurring_connect_minute = ttk.Combobox(time_frame, width=5, values=[f"{i:02d}" for i in range(0, 60, 5)])
        self.recurring_connect_minute.pack(side=tk.LEFT)
        self.recurring_connect_minute.current(0)  # 預設 00 分
        
        # 斷開時間
        tk.Label(self.tab_recurring, text="Disconnect Time:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        time_frame2 = tk.Frame(self.tab_recurring)
        time_frame2.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        self.recurring_disconnect_hour = ttk.Combobox(time_frame2, width=5, values=[f"{i:02d}" for i in range(24)])
        self.recurring_disconnect_hour.pack(side=tk.LEFT)
        self.recurring_disconnect_hour.current(17)  # 預設 17:00
        
        tk.Label(time_frame2, text=":").pack(side=tk.LEFT)
        
        self.recurring_disconnect_minute = ttk.Combobox(time_frame2, width=5, values=[f"{i:02d}" for i in range(0, 60, 5)])
        self.recurring_disconnect_minute.pack(side=tk.LEFT)
        self.recurring_disconnect_minute.current(0)  # 預設 00 分
        
        # 加入排程按鈕
        add_button = tk.Button(self.tab_recurring, text="Add Recurring Schedule", command=self.add_recurring_schedule)
        add_button.grid(row=1, column=3, padx=10, pady=10, sticky="w")
    
    def create_logs_tab(self):
        """建立日誌頁籤內容"""
        # 日誌顯示區域
        log_frame = tk.Frame(self.tab_logs)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 日誌文本框
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, width=70, height=20)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加滾動條
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # 按鈕區域
        button_frame = tk.Frame(self.tab_logs)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 重新整理日誌按鈕
        refresh_button = tk.Button(button_frame, text="Refresh Logs", command=self.refresh_logs)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # 清除日誌按鈕
        clear_button = tk.Button(button_frame, text="Clear Display", command=lambda: self.log_text.delete(1.0, tk.END))
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 載入日誌
        self.refresh_logs()
    
    def create_admin_tab(self):
        """建立管理頁籤內容"""
        # 使用者管理區域
        user_frame = tk.LabelFrame(self.tab_admin, text="User Management")
        user_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 使用者列表
        list_frame = tk.Frame(user_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.user_tree = ttk.Treeview(list_frame, columns=("Username", "Role"), show="headings")
        self.user_tree.heading("Username", text="Username")
        self.user_tree.heading("Role", text="Role")
        self.user_tree.column("Username", width=150)
        self.user_tree.column("Role", width=100)
        self.user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加滾動條
        user_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.user_tree.yview)
        user_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.user_tree.configure(yscrollcommand=user_scrollbar.set)
        
        # 按鈕區域
        button_frame = tk.Frame(user_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 添加使用者按鈕
        add_user_button = tk.Button(button_frame, text="Add User", command=lambda: self.register_new_user(self.root))
        add_user_button.pack(side=tk.LEFT, padx=5)
        
        # 刪除使用者按鈕
        delete_user_button = tk.Button(button_frame, text="Delete User", command=self.delete_user)
        delete_user_button.pack(side=tk.LEFT, padx=5)
        
        # 重設密碼按鈕
        reset_password_button = tk.Button(button_frame, text="Reset Password", command=self.reset_password)
        reset_password_button.pack(side=tk.LEFT, padx=5)
        
        # 載入使用者列表
        self.refresh_user_list()
    
    def refresh_user_list(self):
        """更新使用者列表"""
        # 清空表格
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
            
        # 添加使用者到表格
        for username, user_info in self.users.items():
            self.user_tree.insert('', 'end', values=(username, user_info.get("role", "user")))
    
    def delete_user(self):
        """刪除選中的使用者"""
        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a user to delete")
            return
            
        # 獲取選中的使用者
        values = self.user_tree.item(selected_item[0], 'values')
        username = values[0]
        
        # 不能刪除自己
        if username == self.current_user:
            messagebox.showerror("Error", "You cannot delete your own account")
            return
            
        # 確認刪除
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete user {username}?"):
            # 從使用者列表中刪除
            if username in self.users:
                del self.users[username]
                self.save_users()
                
                # 更新表格
                self.refresh_user_list()
                
                logging.info(f"User {username} deleted by {self.current_user}")
                messagebox.showinfo("Success", f"User {username} deleted successfully")
    
    def reset_password(self):
        """重設選中使用者的密碼"""

        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a user to reset password")
            return
            
        # 獲取選中的使用者
        values = self.user_tree.item(selected_item[0], 'values')
        username = values[0]
        
        # 輸入新密碼
        new_password = simpledialog.askstring("Reset Password", f"Enter new password for {username}:", show='*')
        if not new_password:
            return
            
        # 更新密碼
        if username in self.users:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            self.users[username]["password"] = hashed_password
            self.save_users()
            
            logging.info(f"Password reset for user {username} by {self.current_user}")
            messagebox.showinfo("Success", f"Password for {username} has been reset")
    
    def refresh_logs(self):
        """重新整理日誌顯示"""
        self.log_text.delete(1.0, tk.END)
        
        log_dir = "logs"
        if not os.path.exists(log_dir):
            self.log_text.insert(tk.END, "No logs found.\n")
            return
            
        # 獲取最新的日誌檔案
        log_files = [f for f in os.listdir(log_dir) if f.startswith("nic_scheduler_") and f.endswith(".log")]
        if not log_files:
            self.log_text.insert(tk.END, "No logs found.\n")
            return
            
        # 排序日誌檔案，最新的在前面
        log_files.sort(reverse=True)
        latest_log = os.path.join(log_dir, log_files[0])
        
        # 讀取日誌內容
        try:
            with open(latest_log, 'r') as f:
                log_content = f.readlines()

                # 只顯示最後 100 行
                if len(log_content) > 100:
                    self.log_text.insert(tk.END, f"Showing last 100 lines of {len(log_content)} total lines...\n\n")
                    log_content = log_content[-100:]
                
                for line in log_content:
                    self.log_text.insert(tk.END, line)
                    
                # 滾動到最底部
                self.log_text.see(tk.END)
        except Exception as e:
            self.log_text.insert(tk.END, f"Error reading log file: {e}\n")
    
    def periodic_log_check(self):
        """定期檢查日誌檔案"""
        while not self.stop_thread:
            # 每小時檢查一次日誌檔案大小
            log_dir = "logs"
            if os.path.exists(log_dir):
                current_date = datetime.now().strftime("%Y%m%d")
                log_file = os.path.join(log_dir, f"nic_scheduler_{current_date}.log")
                
                if os.path.exists(log_file):
                    file_size = os.path.getsize(log_file) / (1024 * 1024)  # 轉換為 MB
                    
                    # 如果日誌檔案大於 10MB，發出警告
                    if file_size > 10:
                        logging.warning(f"Log file size is large: {file_size:.2f} MB")
                        
                        # 如果日誌頁籤已經建立，更新警告訊息
                        if hasattr(self, 'log_text'):
                            self.log_text.insert(tk.END, f"\n[WARNING] Log file size is large: {file_size:.2f} MB\n")
                            self.log_text.see(tk.END)
            
            # 休眠 1 小時
            for _ in range(3600):  # 1小時 = 3600秒
                if self.stop_thread:
                    break
                time.sleep(1)
    
    def get_nics(self):
        """獲取網路卡列表"""
        try:
            if os.name == 'nt':  # Windows
                # 使用 PowerShell 獲取更準確的網路卡資訊
                result = subprocess.check_output(
                    'powershell -Command "Get-NetAdapter | Select-Object -Property Name, InterfaceDescription | ConvertTo-Csv -NoTypeInformation"', 
                    shell=True
                ).decode('utf-8', errors='ignore')
                
                lines = result.strip().split('\n')
                if len(lines) <= 1:  # 只有標題行或空
                    return
                    
                headers = lines[0].strip('"').split('","')
                adapters = []
                adapter_details = []
                
                for line in lines[1:]:
                    values = line.strip('"').split('","')
                    if len(values) >= 2:
                        name = values[0]
                        description = values[1]
                        display_text = f"{name} ({description})"
                        adapters.append(display_text)
                        adapter_details.append({"name": name, "description": description})
                
                self.nic_combo['values'] = adapters
                self.adapter_details = adapter_details  # 保存詳細資訊供後續使用
                
                if adapters:
                    self.nic_combo.current(0)
            else:  # Linux/Mac
                result = subprocess.check_output("ifconfig", shell=True).decode()
                adapters = []
                for line in result.split('\n'):
                    if line and not line.startswith(' ') and not line.startswith('\t'):
                        adapter = line.split(':')[0]
                        if adapter:
                            adapters.append(adapter)
                self.nic_combo['values'] = adapters
                if adapters:
                    self.nic_combo.current(0)
                    
            logging.info(f"Successfully retrieved {len(self.nic_combo['values'])} network adapters")
        except Exception as e:
            error_msg = f"Failed to get network adapters: {e}"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def add_to_list(self):
        """添加單次排程到列表"""
        try:
            # 獲取輸入
            selected_index = self.nic_combo.current()
            if selected_index < 0:
                messagebox.showerror("Error", "Please select a NIC")
                return
                
            if os.name == 'nt' and hasattr(self, 'adapter_details') and self.adapter_details:
                # 使用實際的網路卡名稱而非顯示名稱
                nic = self.adapter_details[selected_index]["name"]
                nic_display = self.nic_combo.get()  # 顯示用
            else:
                nic = self.nic_combo.get()
                nic_display = nic
                
            date_str = self.date_entry.get()
            connect_time = f"{self.connect_hour.get()}:{self.connect_minute.get()}"
            disconnect_time = f"{self.disconnect_hour.get()}:{self.disconnect_minute.get()}"
            
            # 驗證輸入
            if not nic:
                messagebox.showerror("Error", "Please select a NIC")
                return
                
            try:
                date_obj = datetime.strptime(date_str, "%Y/%m/%d")
                
                # 檢查日期是否已過期
                if date_obj.date() < datetime.now().date():
                    messagebox.showerror("Error", "Cannot schedule for past dates")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY/MM/DD")
                return
                
            # 檢查是否已存在
            for schedule in self.schedules:
                if schedule['date'] == date_str and schedule['nic'] == nic and not schedule.get('recurring', False):
                    messagebox.showerror("Error", "This date and NIC combination is already scheduled")
                    return
            
            # 添加到排程列表
            schedule_item = {
                'nic': nic,  # 實際網路卡名稱
                'nic_display': nic_display,  # 顯示用名稱
                'date': date_str,
                'connect': connect_time,
                'disconnect': disconnect_time,
                'recurring': False,  # 標記為單次排程
                'type': 'single'  # 排程類型
            }
            self.schedules.append(schedule_item)
            
            # 更新表格 - 使用顯示名稱
            self.schedule_tree.insert('', 'end', values=(date_str, connect_time, disconnect_time, nic_display, "Single"))
            
            # 自動保存
            self.save_schedules()
            
            # 更新排程
            self.update_scheduler()
            
            logging.info(f"Added single schedule for NIC {nic} on {date_str}, connect: {connect_time}, disconnect: {disconnect_time}")
            
        except Exception as e:
            error_msg = f"Failed to add schedule: {e}"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def add_recurring_schedule(self):
        """添加週期性排程到列表"""
        try:
            # 獲取輸入
            selected_index = self.recurring_nic_combo.current()
            if selected_index < 0:
                messagebox.showerror("Error", "Please select a NIC")
                return
                
            if os.name == 'nt' and hasattr(self, 'adapter_details') and self.adapter_details:
                # 使用實際的網路卡名稱而非顯示名稱
                nic = self.adapter_details[selected_index]["name"]
                nic_display = self.recurring_nic_combo.get()  # 顯示用
            else:
                nic = self.recurring_nic_combo.get()
                nic_display = nic
                
            connect_time = f"{self.recurring_connect_hour.get()}:{self.recurring_connect_minute.get()}"
            disconnect_time = f"{self.recurring_disconnect_hour.get()}:{self.recurring_disconnect_minute.get()}"
            
            # 獲取選中的星期幾
            selected_days = []
            day_names = []
            for i, var in enumerate(self.day_vars):
                if var.get():
                    selected_days.append(i)  # 0-6 表示週一至週日
                    day_name = calendar.day_name[i][:3]  # 獲取星期幾的縮寫
                    day_names.append(day_name)
            
            if not selected_days:
                messagebox.showerror("Error", "Please select at least one day of the week")
                return
                
            # 驗證輸入
            if not nic:
                messagebox.showerror("Error", "Please select a NIC")
                return
                
            # 檢查是否已存在
            day_str = ",".join(day_names)
            for schedule in self.schedules:
                if (schedule.get('recurring', False) and 
                    schedule['nic'] == nic and 
                    schedule.get('days', []) == selected_days):
                    messagebox.showerror("Error", "This recurring schedule already exists")
                    return
            
            # 添加到排程列表
            schedule_item = {
                'nic': nic,  # 實際網路卡名稱
                'nic_display': nic_display,  # 顯示用名稱
                'connect': connect_time,
                'disconnect': disconnect_time,
                'recurring': True,  # 標記為週期性排程
                'days': selected_days,  # 星期幾 (0-6)
                'day_names': day_names,  # 星期幾的名稱
                'type': 'recurring'  # 排程類型
            }
            self.schedules.append(schedule_item)
            
            # 更新表格 - 使用顯示名稱
            self.schedule_tree.insert('', 'end', values=(day_str, connect_time, disconnect_time, nic_display, "Recurring"))
            
            # 自動保存
            self.save_schedules()
            
            # 更新排程
            self.update_scheduler()
            
            logging.info(f"Added recurring schedule for NIC {nic} on days {day_str}, connect: {connect_time}, disconnect: {disconnect_time}")
            
        except Exception as e:
            error_msg = f"Failed to add recurring schedule: {e}"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def delete_selected(self):
        """刪除選中的排程"""
        selected_item = self.schedule_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a schedule to delete")
            return
            
        # 從表格和列表中刪除
        for item in selected_item:
            values = self.schedule_tree.item(item, 'values')
            date_or_days = values[0]
            nic_display = values[3]
            schedule_type = values[4]
            
            # 從列表中刪除
            if schedule_type == "Single":
                # 單次排程，根據日期刪除
                self.schedules = [s for s in self.schedules if s.get('date', '') != date_or_days or s.get('type', '') != 'single']
                logging.info(f"Deleted single schedule for date {date_or_days}, NIC: {nic_display}")
            else:
                # 週期性排程，根據星期幾刪除
                day_names = date_or_days.split(',')
                self.schedules = [s for s in self.schedules if not (s.get('recurring', False) and all(day in s.get('day_names', []) for day in day_names))]
                logging.info(f"Deleted recurring schedule for days {date_or_days}, NIC: {nic_display}")
            
            # 從表格中刪除
            self.schedule_tree.delete(item)
        
        # 保存並更新排程
        self.save_schedules()
        self.update_scheduler()
    
    def save_schedules(self):
        """保存排程到檔案"""
        try:
            with open(self.schedule_file, 'w') as f:
                json.dump(self.schedules, f)
            logging.info(f"Schedules saved successfully. Total schedules: {len(self.schedules)}")
        except Exception as e:
            error_msg = f"Failed to save schedules: {e}"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def load_schedules(self):
        """從檔案載入排程"""
        try:
            if os.path.exists(self.schedule_file):
                with open(self.schedule_file, 'r') as f:
                    self.schedules = json.load(f)
                    
                # 過濾掉已過期的單次排程
                current_date = datetime.now().strftime("%Y/%m/%d")
                self.schedules = [s for s in self.schedules if s.get('recurring', False) or s.get('date', '') >= current_date]
                
                logging.info(f"Loaded {len(self.schedules)} schedules from file")
            else:
                # 如果檔案不存在，初始化為空列表
                self.schedules = []
                logging.info("Schedule file not found, initialized empty schedule list")
        except Exception as e:
            error_msg = f"Failed to load schedules: {e}"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
            self.schedules = []
    
    def refresh_schedule_list(self):
        """更新排程表格"""
        # 清空表格
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)
            
        # 添加排程到表格
        for schedule in self.schedules:
            if schedule.get('recurring', False):
                # 週期性排程
                day_str = ",".join(schedule.get('day_names', []))
                self.schedule_tree.insert('', 'end', values=(
                    day_str,
                    schedule.get('connect', ''),
                    schedule.get('disconnect', ''),
                    schedule.get('nic_display', schedule.get('nic', '')),
                    "Recurring"
                ))
            else:
                # 單次排程
                self.schedule_tree.insert('', 'end', values=(
                    schedule.get('date', ''),
                    schedule.get('connect', ''),
                    schedule.get('disconnect', ''),
                    schedule.get('nic_display', schedule.get('nic', '')),
                    "Single"
                ))
    
    def update_scheduler(self):
        """更新排程器"""
        # 清除所有排程
        schedule.clear()
        
        # 過濾有效排程
        current_date = datetime.now().strftime("%Y/%m/%d")
        valid_schedules = [s for s in self.schedules if s.get('recurring', False) or s.get('date', '') >= current_date]
        
        # 添加新排程
        for s in valid_schedules:
            try:
                # 獲取排程資訊
                connect_time = s.get('connect', '')
                disconnect_time = s.get('disconnect', '')
                nic = s.get('nic', '')
                
                if s.get('recurring', False):
                    # 週期性排程
                    days = s.get('days', [])
                    for day_index in days:
                        # 根據星期幾設定排程
                        if day_index == 0:  # 週一
                            schedule.every().monday.at(connect_time).do(
                                self.enable_nic, nic, "recurring", connect_time
                            )
                            schedule.every().monday.at(disconnect_time).do(
                                self.disable_nic, nic, "recurring", disconnect_time
                            )
                        elif day_index == 1:  # 週二
                            schedule.every().tuesday.at(connect_time).do(
                                self.enable_nic, nic, "recurring", connect_time
                            )
                            schedule.every().tuesday.at(disconnect_time).do(
                                self.disable_nic, nic, "recurring", disconnect_time
                            )
                        elif day_index == 2:  # 週三
                            schedule.every().wednesday.at(connect_time).do(
                                self.enable_nic, nic, "recurring", connect_time
                            )
                            schedule.every().wednesday.at(disconnect_time).do(
                                self.disable_nic, nic, "recurring", disconnect_time
                            )
                        elif day_index == 3:  # 週四
                            schedule.every().thursday.at(connect_time).do(
                                self.enable_nic, nic, "recurring", connect_time
                            )
                            schedule.every().thursday.at(disconnect_time).do(
                                self.disable_nic, nic, "recurring", disconnect_time
                            )
                        elif day_index == 4:  # 週五
                            schedule.every().friday.at(connect_time).do(
                                self.enable_nic, nic, "recurring", connect_time
                            )
                            schedule.every().friday.at(disconnect_time).do(
                                self.disable_nic, nic, "recurring", disconnect_time
                            )
                        elif day_index == 5:  # 週六
                            schedule.every().saturday.at(connect_time).do(
                                self.enable_nic, nic, "recurring", connect_time
                            )
                            schedule.every().saturday.at(disconnect_time).do(
                                self.disable_nic, nic, "recurring", disconnect_time
                            )
                        elif day_index == 6:  # 週日
                            schedule.every().sunday.at(connect_time).do(
                                self.enable_nic, nic, "recurring", connect_time
                            )
                            schedule.every().sunday.at(disconnect_time).do(
                                self.disable_nic, nic, "recurring", disconnect_time
                            )
                else:
                    # 單次排程
                    date_str = s.get('date', '')
                    
                    # 添加連接排程
                    connect_job = schedule.every().day.at(connect_time).do(
                        self.enable_nic, nic, date_str, connect_time
                    )
                    
                    # 添加斷開排程
                    disconnect_job = schedule.every().day.at(disconnect_time).do(
                        self.disable_nic, nic, date_str, disconnect_time
                    )
            except KeyError as e:
                error_msg = f"Schedule item missing required key: {e}, item: {s}"
                logging.error(error_msg)
            except Exception as e:
                error_msg = f"Error processing schedule: {e}, item: {s}"
                logging.error(error_msg)
        
        # 立即更新 Next Check 顯示
        next_run = schedule.next_run()
        if next_run:
            next_run_str = next_run.strftime("%Y/%m/%d %H:%M:%S")
            self.status_label.config(text=f"Next check: {next_run_str}")
        else:
            self.status_label.config(text="No scheduled tasks")
    
    def enable_nic(self, nic, date, time):
        """啟用網路卡"""
        try:
            # 檢查日期是否匹配 (週期性排程不需要檢查)
            if date != "recurring":
                current_date = datetime.now().strftime("%Y/%m/%d")
                if current_date != date:
                    logging.debug(f"Date mismatch: current {current_date}, scheduled {date}")
                    return
                    
            # 先執行網路卡啟用操作
            if os.name == 'nt':  # Windows
                result = subprocess.run(
                    f'powershell -Command "Enable-NetAdapter -Name \'{nic}\' -Confirm:$false"', 
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    # 嘗試使用模糊匹配
                    result = subprocess.run(
                        f'powershell -Command "Get-NetAdapter | Where-Object {{ $_.Name -eq \'{nic}\' }} | Enable-NetAdapter -Confirm:$false"', 
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        raise Exception(f"PowerShell error: {result.stderr}")
            else:  # Linux
                subprocess.run(f'ifconfig {nic} up', shell=True)
                
            # 記錄操作
            if date == "recurring":
                logging.info(f"NIC {nic} enabled at {time} (recurring schedule for {datetime.now().strftime('%A')})")
            else:
                logging.info(f"NIC {nic} enabled at {time} (scheduled for {date})")
                
            # 操作成功後，非阻塞式顯示訊息框
            self.show_non_blocking_message("NIC Enabled", f"NIC {nic} has been enabled at {time}")
        except Exception as e:
            error_msg = f"Failed to enable NIC {nic}: {e}"
            logging.error(error_msg)
            # 錯誤訊息仍然使用阻塞式顯示，因為這是需要用戶注意的
            messagebox.showerror("Error", error_msg)
    
    def disable_nic(self, nic, date, time):
        """禁用網路卡"""
        try:
            # 檢查日期是否匹配 (週期性排程不需要檢查)
            if date != "recurring":
                current_date = datetime.now().strftime("%Y/%m/%d")
                if current_date != date:
                    logging.debug(f"Date mismatch: current {current_date}, scheduled {date}")
                    return
                    
            # 先執行網路卡禁用操作
            if os.name == 'nt':  # Windows
                result = subprocess.run(
                    f'powershell -Command "Disable-NetAdapter -Name \'{nic}\' -Confirm:$false"', 
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    # 嘗試使用模糊匹配
                    result = subprocess.run(
                        f'powershell -Command "Get-NetAdapter | Where-Object {{ $_.Name -eq \'{nic}\' }} | Disable-NetAdapter -Confirm:$false"', 
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        raise Exception(f"PowerShell error: {result.stderr}")
            else:  # Linux
                subprocess.run(f'ifconfig {nic} down', shell=True)
                
            # 記錄操作
            if date == "recurring":
                logging.info(f"NIC {nic} disabled at {time} (recurring schedule for {datetime.now().strftime('%A')})")
            else:
                logging.info(f"NIC {nic} disabled at {time} (scheduled for {date})")
                
            # 操作成功後，非阻塞式顯示訊息框
            self.show_non_blocking_message("NIC Disabled", f"NIC {nic} has been disabled at {time}")
        except Exception as e:
            error_msg = f"Failed to disable NIC {nic}: {e}"
            logging.error(error_msg)
            # 錯誤訊息仍然使用阻塞式顯示，因為這是需要用戶注意的
            messagebox.showerror("Error", error_msg)
    
    def show_non_blocking_message(self, title, message):
        """顯示非阻塞式訊息框"""
        # 創建一個新的頂層窗口
        msg_window = tk.Toplevel(self.root)
        msg_window.title(title)
        msg_window.geometry("300x150")
        
        # 置中顯示
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 150) // 2
        msg_window.geometry(f"300x150+{x}+{y}")
        
        # 添加圖標
        info_frame = tk.Frame(msg_window)
        info_frame.pack(pady=10)
        
        # 使用 Unicode 字符作為信息圖標
        tk.Label(info_frame, text="ℹ️", font=("Arial", 24)).pack(side=tk.LEFT, padx=10)
        
        # 添加訊息
        tk.Label(msg_window, text=message, wraplength=250).pack(pady=10)
        
        # 添加 OK 按鈕
        tk.Button(msg_window, text="OK", command=msg_window.destroy).pack(pady=10)
        
        # 設置窗口在最上層
        msg_window.attributes('-topmost', True)
        
        # 3秒後自動關閉
        msg_window.after(3000, msg_window.destroy)
    
    def test_nic_operations(self):
        """測試網路卡操作"""
        selected_index = self.nic_combo.current()
        if selected_index < 0:
            messagebox.showerror("Error", "Please select a NIC")
            return
            
        if os.name == 'nt' and hasattr(self, 'adapter_details') and self.adapter_details:
            nic = self.adapter_details[selected_index]["name"]
        else:
            nic = self.nic_combo.get()
            
        try:
            # 顯示確認對話框
            if messagebox.askyesno("Confirm", f"This will test disabling and enabling the selected NIC ({nic}).\nContinue?"):
                logging.info(f"Starting NIC operations test for {nic}")
                
                # 禁用網路卡
                if os.name == 'nt':
                    result = subprocess.run(
                        f'powershell -Command "Disable-NetAdapter -Name \'{nic}\' -Confirm:$false"', 
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        # 嘗試使用模糊匹配
                        result = subprocess.run(
                            f'powershell -Command "Get-NetAdapter | Where-Object {{ $_.Name -eq \'{nic}\' }} | Disable-NetAdapter -Confirm:$false"', 
                            shell=True,
                            capture_output=True,
                            text=True
                        )

                        if result.returncode != 0:
                            raise Exception(f"PowerShell error: {result.stderr}")
                    
                    # 顯示非阻塞式訊息
                    self.show_non_blocking_message("Test", f"NIC {nic} disabled, will enable in 3 seconds")
                    logging.info(f"NIC {nic} disabled for testing")
                    
                    # 等待3秒
                    time.sleep(3)
                    
                    # 啟用網路卡
                    result = subprocess.run(
                        f'powershell -Command "Enable-NetAdapter -Name \'{nic}\' -Confirm:$false"', 
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        # 嘗試使用模糊匹配
                        result = subprocess.run(
                            f'powershell -Command "Get-NetAdapter | Where-Object {{ $_.Name -eq \'{nic}\' }} | Enable-NetAdapter -Confirm:$false"', 
                            shell=True,
                            capture_output=True,
                            text=True
                        )
                        if result.returncode != 0:
                            raise Exception(f"PowerShell error: {result.stderr}")
                    
                    # 顯示非阻塞式成功訊息
                    self.show_non_blocking_message("Success", "NIC operations test completed successfully")
                    logging.info(f"NIC {nic} enabled after testing, test completed successfully")
                else:
                    # Linux 代碼
                    subprocess.run(f'ifconfig {nic} down', shell=True)
                    self.show_non_blocking_message("Test", f"NIC {nic} disabled, will enable in 3 seconds")
                    logging.info(f"NIC {nic} disabled for testing")
                    time.sleep(3)
                    subprocess.run(f'ifconfig {nic} up', shell=True)
                    self.show_non_blocking_message("Success", "NIC operations test completed successfully")
                    logging.info(f"NIC {nic} enabled after testing, test completed successfully")
        except Exception as e:
            error_msg = f"Test failed: {e}"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)

    def run_scheduler(self):
        """運行排程器線程"""
        while not self.stop_thread:
            schedule.run_pending()
            
            # 更新下次檢查時間
            next_run = schedule.next_run()
            if next_run:
                next_run_str = next_run.strftime("%Y/%m/%d %H:%M:%S")
                self.status_label.config(text=f"Next check: {next_run_str}")
            else:
                self.status_label.config(text="No scheduled tasks")
                
            time.sleep(1)
    
    def run(self):
        """運行主程序"""
        self.update_scheduler()  # 初始化排程
        self.root.mainloop()
        
        # 停止排程線程
        self.stop_thread = True
        if self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=1)
        if hasattr(self, 'log_check_thread') and self.log_check_thread.is_alive():
            self.log_check_thread.join(timeout=1)

if __name__ == "__main__":
    app = NICScheduler()
    app.run()