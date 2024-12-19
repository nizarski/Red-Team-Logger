import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime
import pytz
import time

class RedTeamLogger:
    def __init__(self, root):
        self.root = root
        self.root.title("Red Team Logger")

        self.assets = []
        self.operations = []
        self.timezone = pytz.timezone("UTC")
        self.kill_chain_steps = [
            "Initial Access", "Execution", "Persistence", "Privilege Escalation",
            "Defense Evasion", "Credential Access", "Discovery", "Lateral Movement",
            "Collection", "Exfiltration", "Command and Control"
        ]

        self.setup_gui()

    def setup_gui(self):
        tz_frame = ttk.LabelFrame(self.root, text="Timezone")
        tz_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(tz_frame, text="Current Timezone:").grid(row=0, column=0, padx=5, pady=5)
        self.tz_var = tk.StringVar(value=self.timezone.zone)
        self.tz_label = ttk.Label(tz_frame, textvariable=self.tz_var)
        self.tz_label.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(tz_frame, text="Select Timezone:").grid(row=1, column=0, padx=5, pady=5)
        self.manual_tz_var = tk.StringVar()
        self.timezones = sorted(pytz.all_timezones)
        self.tz_combobox = ttk.Combobox(tz_frame, textvariable=self.manual_tz_var, values=self.timezones, state="readonly", width=30)
        self.tz_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.tz_combobox.bind("<<ComboboxSelected>>", self.set_timezone)

        assets_frame = ttk.LabelFrame(self.root, text="Assets")
        assets_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.asset_entry = ttk.Entry(assets_frame, width=40)
        self.asset_entry.grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(assets_frame, text="Add Asset", command=self.add_asset).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(assets_frame, text="Delete Selected", command=self.delete_asset).grid(row=0, column=2, padx=5, pady=5)
        
        self.asset_listbox = tk.Listbox(assets_frame, height=5, width=50, selectmode="single")
        self.asset_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        operations_frame = ttk.LabelFrame(self.root, text="Operations")
        operations_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(operations_frame, text="Command:").grid(row=0, column=0, padx=5, pady=5)
        self.command_entry = ttk.Entry(operations_frame, width=40)
        self.command_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(operations_frame, text="Kill Chain Step (Optional):").grid(row=1, column=0, padx=5, pady=5)
        self.kill_chain_var = tk.StringVar()
        self.kill_chain_combobox = ttk.Combobox(operations_frame, textvariable=self.kill_chain_var, values=self.kill_chain_steps, state="readonly", width=30)
        self.kill_chain_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(operations_frame, text="Targeted Assets:").grid(row=2, column=0, padx=5, pady=5)
        self.target_assets_listbox = tk.Listbox(operations_frame, selectmode="multiple", height=5, width=40)
        self.target_assets_listbox.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(operations_frame, text="Log Operation", command=self.log_operation).grid(row=3, column=0, columnspan=2, pady=5)

        logs_frame = ttk.LabelFrame(self.root, text="Logged Data")
        logs_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.logs_text = tk.Text(logs_frame, height=10, width=70, state="disabled")
        self.logs_text.grid(row=0, column=0, padx=5, pady=5)

        export_button = ttk.Button(self.root, text="Export to CSV", command=self.export_to_csv)
        export_button.grid(row=4, column=0, padx=10, pady=10)

    def set_timezone(self, event=None):
        try:
            self.timezone = pytz.timezone(self.manual_tz_var.get())
            self.tz_var.set(self.timezone.zone)
            messagebox.showinfo("Success", f"Timezone set to {self.timezone.zone}")
        except pytz.UnknownTimeZoneError:
            messagebox.showerror("Error", "Invalid timezone. Please try again.")

    def add_asset(self):
        asset = self.asset_entry.get().strip()
        if asset:
            self.assets.append(asset)
            self.asset_listbox.insert(tk.END, asset)
            self.target_assets_listbox.insert(tk.END, asset)
            self.asset_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Asset cannot be empty.")

    def delete_asset(self):
        selected = self.asset_listbox.curselection()
        if selected:
            index = selected[0]
            asset = self.assets.pop(index)
            self.asset_listbox.delete(index)

            for i in range(self.target_assets_listbox.size()):
                if self.target_assets_listbox.get(i) == asset:
                    self.target_assets_listbox.delete(i)
                    break
        else:
            messagebox.showerror("Error", "No asset selected to delete.")

    def log_operation(self):
        command = self.command_entry.get().strip()
        selected_indices = self.target_assets_listbox.curselection()
        targets = [self.target_assets_listbox.get(i) for i in selected_indices]
        kill_chain_step = self.kill_chain_var.get().strip()
        
        if command and targets:
            timestamp = datetime.now(self.timezone).strftime("%Y-%m-%d %I:%M:%S %p")
            operation = {
                "Timestamp": timestamp,
                "Command": command,
                "Targets": ", ".join(targets),
                "Kill Chain Step": kill_chain_step if kill_chain_step else "N/A"
            }
            self.operations.append(operation)
            self.display_logs()
            self.command_entry.delete(0, tk.END)
            self.kill_chain_combobox.set("")
        else:
            messagebox.showerror("Error", "Command and Targeted Assets cannot be empty.")

    def display_logs(self):
        self.logs_text.config(state="normal")
        self.logs_text.delete("1.0", tk.END)
        for op in self.operations:
            log_entry = f"{op['Timestamp']} : {op['Command']} (Targets: {op['Targets']}, Kill Chain: {op['Kill Chain Step']})\n"
            self.logs_text.insert(tk.END, log_entry)
        self.logs_text.config(state="disabled")

    def export_to_csv(self):
        if not self.operations:
            messagebox.showerror("Error", "No operations to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            df = pd.DataFrame(self.operations)
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", f"Data exported to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RedTeamLogger(root)
    root.mainloop()
