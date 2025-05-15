# NIC-Scheduler Installation Guide

## System Requirements
- Python 3.6 or higher
- Windows 7/10/11 or Linux/macOS

## Installation Steps

### Windows
1. Install Python (if not already installed)
   - Download and install from [Python official website](https://www.python.org/downloads/)
   - Check "Add Python to PATH" during installation

2. Download NIC-Scheduler
   ```
   git clone https://github.com/RoidaChung/nic-scheduler.git
   cd nic-scheduler
   ```

3. Install Dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run the Program
   ```
   python nic-scheduler.py
   ```

### Linux/macOS
1. Install Python (if not already installed)
   ```
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip

   # macOS
   brew install python
   ```

2. Download NIC-Scheduler
   ```
   git clone https://github.com/RoidaChung/nic-scheduler.git
   cd nic-scheduler
   ```

3. Install Dependencies
   ```
   pip3 install -r requirements.txt
   ```

4. Run the Program
   ```
   python3 nic-scheduler.py
   ```

## Set Up Autostart at Boot

### Windows
1. Create a batch file `start_nic_scheduler.bat`
   ```
   @echo off
   cd path\to\nic-scheduler
   python nic-scheduler.py
   ```

2. Place a shortcut to the batch file in the startup folder
   - Press Win+R, type `shell:startup`, then place the shortcut in the opened folder

### Linux
1. Create a service file
   ```
   sudo nano /etc/systemd/system/nic-scheduler.service
   ```

2. Add the following content
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

3. Enable the service
   ```
   sudo systemctl enable nic-scheduler.service
   sudo systemctl start nic-scheduler.service
   ```