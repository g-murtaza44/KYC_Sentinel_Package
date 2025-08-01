#!/usr/bin/env python3
"""
KYC Sentinel - Desktop Application for KYC/AML Compliance Screening
Author: Senior Python Developer
Description: GUI-based tool for screening names against OpenSanctions API
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import requests
import json
from datetime import datetime
import os
from openpyxl import Workbook
from openpyxl.styles import PatternFill
import threading
import time

class KYCSentinelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KYC Sentinel - Compliance Screening Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="KYC Sentinel", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        subtitle_label = ttk.Label(main_frame, text="KYC/AML Compliance Screening Tool", font=("Arial", 12))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # Mode selection
        mode_frame = ttk.LabelFrame(main_frame, text="Select Mode", padding="10")
        mode_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        mode_frame.columnconfigure(1, weight=1)
        
        self.mode_var = tk.StringVar(value="manual")
        
        manual_radio = ttk.Radiobutton(mode_frame, text="Manual Mode", variable=self.mode_var, 
                                      value="manual", command=self.toggle_mode)
        manual_radio.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        batch_radio = ttk.Radiobutton(mode_frame, text="Batch Mode (CSV)", variable=self.mode_var, 
                                     value="batch", command=self.toggle_mode)
        batch_radio.grid(row=0, column=1, sticky=tk.W)
        
        # Manual input frame
        self.manual_frame = ttk.LabelFrame(main_frame, text="Manual Input", padding="15")
        self.manual_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        self.manual_frame.columnconfigure(1, weight=1)
        
        # Manual input fields
        ttk.Label(self.manual_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(self.manual_frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(self.manual_frame, text="Date of Birth:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dob_entry = ttk.Entry(self.manual_frame, width=40)
        self.dob_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.dob_entry.insert(0, "DD/MM/YYYY")
        
        ttk.Label(self.manual_frame, text="CNIC:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cnic_entry = ttk.Entry(self.manual_frame, width=40)
        self.cnic_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Manual check button
        self.manual_check_btn = ttk.Button(self.manual_frame, text="Run Check", 
                                          command=self.run_manual_check)
        self.manual_check_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Batch input frame
        self.batch_frame = ttk.LabelFrame(main_frame, text="Batch Processing", padding="15")
        self.batch_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        self.batch_frame.columnconfigure(0, weight=1)
        
        # CSV file selection
        self.csv_frame = ttk.Frame(self.batch_frame)
        self.csv_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        self.csv_frame.columnconfigure(0, weight=1)
        
        self.csv_path_var = tk.StringVar()
        self.csv_entry = ttk.Entry(self.csv_frame, textvariable=self.csv_path_var, state="readonly")
        self.csv_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.browse_btn = ttk.Button(self.csv_frame, text="Browse CSV", command=self.browse_csv)
        self.browse_btn.grid(row=0, column=1)
        
        # Batch check button
        self.batch_check_btn = ttk.Button(self.batch_frame, text="Upload CSV & Run Bulk Check", 
                                         command=self.run_batch_check)
        self.batch_check_btn.grid(row=1, column=0, pady=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 10))
        self.status_label.grid(row=6, column=0, columnspan=2)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        self.results_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=20)
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
        
        # Results text area
        self.results_text = tk.Text(self.results_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure row weights for expansion
        main_frame.rowconfigure(7, weight=1)
        
        # Initialize mode
        self.toggle_mode()
        
    def toggle_mode(self):
        """Toggle between manual and batch modes"""
        if self.mode_var.get() == "manual":
            self.manual_frame.grid()
            self.batch_frame.grid_remove()
        else:
            self.manual_frame.grid_remove()
            self.batch_frame.grid()
    
    def browse_csv(self):
        """Open file dialog to select CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.csv_path_var.set(file_path)
    
    def check_name_against_opensanctions(self, name):
        """Check a name against OpenSanctions API"""
        try:
            url = f"https://api.opensanctions.org/match?q={name}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            matches = data.get('matches', [])
            
            if matches:
                return "Match Found", matches
            else:
                return "Clear", []
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Invalid response from API")
    
    def run_manual_check(self):
        """Run KYC check for manual input"""
        name = self.name_entry.get().strip()
        dob = self.dob_entry.get().strip()
        cnic = self.cnic_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter a name")
            return
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.status_var.set("Checking...")
        self.progress_var.set(50)
        self.root.update()
        
        try:
            status, matches = self.check_name_against_opensanctions(name)
            
            # Display results
            result_text = f"Name: {name}\n"
            result_text += f"DOB: {dob if dob and dob != 'DD/MM/YYYY' else 'Not provided'}\n"
            result_text += f"CNIC: {cnic if cnic else 'Not provided'}\n"
            result_text += f"Status: {status}\n"
            result_text += "-" * 50 + "\n"
            
            if matches:
                result_text += f"Found {len(matches)} potential matches:\n\n"
                for i, match in enumerate(matches[:3], 1):  # Show first 3 matches
                    result_text += f"Match {i}:\n"
                    result_text += f"  Name: {match.get('name', 'N/A')}\n"
                    result_text += f"  Dataset: {match.get('dataset', 'N/A')}\n"
                    result_text += f"  Score: {match.get('score', 'N/A')}\n\n"
            
            self.results_text.insert(tk.END, result_text)
            
            # Save to Excel
            self.save_single_result_to_excel(name, dob, cnic, status)
            
            self.status_var.set("Check completed successfully")
            self.progress_var.set(100)
            
        except Exception as e:
            messagebox.showerror("Error", f"Check failed: {str(e)}")
            self.status_var.set("Check failed")
            self.progress_var.set(0)
    
    def run_batch_check(self):
        """Run KYC check for batch CSV input"""
        csv_path = self.csv_path_var.get()
        
        if not csv_path:
            messagebox.showerror("Error", "Please select a CSV file")
            return
        
        # Run in separate thread to prevent UI freezing
        thread = threading.Thread(target=self._process_batch_check, args=(csv_path,))
        thread.daemon = True
        thread.start()
    
    def _process_batch_check(self, csv_path):
        """Process batch check in separate thread"""
        try:
            # Read CSV
            self.status_var.set("Reading CSV file...")
            self.progress_var.set(10)
            self.root.update()
            
            df = pd.read_csv(csv_path)
            
            # Validate CSV columns
            required_columns = ['Name', 'DOB', 'CNIC']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                messagebox.showerror("Error", f"CSV missing required columns: {', '.join(missing_columns)}")
                return
            
            results = []
            total_rows = len(df)
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Processing {total_rows} records...\n\n")
            self.root.update()
            
            for index, row in df.iterrows():
                try:
                    name = str(row['Name']).strip()
                    dob = str(row['DOB']).strip() if pd.notna(row['DOB']) else ""
                    cnic = str(row['CNIC']).strip() if pd.notna(row['CNIC']) else ""
                    
                    if not name or name.lower() == 'nan':
                        status = "Error: No name provided"
                        matches = []
                    else:
                        status, matches = self.check_name_against_opensanctions(name)
                    
                    results.append({
                        'Name': name,
                        'DOB': dob,
                        'CNIC': cnic,
                        'Status': status
                    })
                    
                    # Update progress
                    progress = ((index + 1) / total_rows) * 80 + 10  # 10-90%
                    self.progress_var.set(progress)
                    
                    # Update results display
                    result_line = f"{index + 1}. {name} - {status}\n"
                    self.results_text.insert(tk.END, result_line)
                    self.results_text.see(tk.END)
                    self.root.update()
                    
                    # Small delay to prevent API rate limiting
                    time.sleep(0.1)
                    
                except Exception as e:
                    results.append({
                        'Name': name if 'name' in locals() else 'Unknown',
                        'DOB': dob if 'dob' in locals() else '',
                        'CNIC': cnic if 'cnic' in locals() else '',
                        'Status': f"Error: {str(e)}"
                    })
            
            # Save results to Excel
            self.status_var.set("Saving results to Excel...")
            self.progress_var.set(90)
            self.root.update()
            
            self.save_batch_results_to_excel(results)
            
            self.status_var.set(f"Batch processing completed. {len(results)} records processed.")
            self.progress_var.set(100)
            
            self.results_text.insert(tk.END, f"\nProcessing completed! Results saved to output/KYC_Results.xlsx")
            self.results_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Batch processing failed: {str(e)}")
            self.status_var.set("Batch processing failed")
            self.progress_var.set(0)
    
    def save_single_result_to_excel(self, name, dob, cnic, status):
        """Save single result to Excel file"""
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "KYC Results"
            
            # Headers
            headers = ['Name', 'DOB', 'CNIC', 'Status']
            for col, header in enumerate(headers, 1):
                ws.cell(row=1, column=col, value=header)
            
            # Data
            ws.cell(row=2, column=1, value=name)
            ws.cell(row=2, column=2, value=dob if dob and dob != 'DD/MM/YYYY' else '')
            ws.cell(row=2, column=3, value=cnic)
            ws.cell(row=2, column=4, value=status)
            
            # Highlight matches in red
            if status == "Match Found":
                red_fill = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")
                for col in range(1, 5):
                    ws.cell(row=2, column=col).fill = red_fill
            
            # Auto-adjust column widths
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column].width = adjusted_width
            
            # Save file
            output_path = "output/KYC_Results.xlsx"
            wb.save(output_path)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save Excel file: {str(e)}")
    
    def save_batch_results_to_excel(self, results):
        """Save batch results to Excel file"""
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "KYC Results"
            
            # Headers
            headers = ['Name', 'DOB', 'CNIC', 'Status']
            for col, header in enumerate(headers, 1):
                ws.cell(row=1, column=col, value=header)
            
            # Data
            red_fill = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")
            
            for row_idx, result in enumerate(results, 2):
                ws.cell(row=row_idx, column=1, value=result['Name'])
                ws.cell(row=row_idx, column=2, value=result['DOB'])
                ws.cell(row=row_idx, column=3, value=result['CNIC'])
                ws.cell(row=row_idx, column=4, value=result['Status'])
                
                # Highlight matches in red
                if result['Status'] == "Match Found":
                    for col in range(1, 5):
                        ws.cell(row=row_idx, column=col).fill = red_fill
            
            # Auto-adjust column widths
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column].width = adjusted_width
            
            # Save file
            output_path = "output/KYC_Results.xlsx"
            wb.save(output_path)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save Excel file: {str(e)}")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = KYCSentinelApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()