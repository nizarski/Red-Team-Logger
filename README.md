# Red Team Logger Tool

## Overview
The **Red Team Logger Tool** is a Python-based application with a GUI that facilitates efficient and structured logging of operations during red team exercises. It supports tracking commands, associated assets, and cyber kill chain steps, along with automatic timezone detection and manual timezone selection. Logs can be exported as CSV files for further analysis.

---

## Features

1. **Automatic Timezone Detection**:
   - The tool automatically detects the system's timezone and uses it for timestamps.

2. **Manual Timezone Selection**:
   - Users can override the default timezone using a dropdown list of all available timezones.

3. **Asset Management**:
   - Add, delete, and edit a list of targeted assets.

4. **Operation Logging**:
   - Record operations with the following details:
     - **Timestamp**
     - **Command**
     - **Targeted Assets** (multiple selections allowed)
     - **Cyber Kill Chain Step** (optional, such as "Initial Access," "Lateral Movement," etc.)

5. **Log Export**:
   - Export all logged operations to a CSV file for reporting or analysis.

6. **GUI-Based Interface**:
   - Easy-to-use graphical interface built with `tkinter`.

---

## Installation

### Prerequisites
- Python 3.8+
- Required Python libraries:
  - `tkinter` (usually included with Python)
  - `pandas`
  - `pytz`

### Steps
1. Clone or download the repository:
   ```bash
   git clone https://github.com/nizarski/Red-Team-Logger.git
   cd Red-Team-Logger
   pip3 install -r requirements.txt
   python3 main.py
