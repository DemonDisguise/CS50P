import customtkinter as ctk
import sqlite3
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime
import zipfile
import os

# Initialize customtkinter appearance
ctk.set_appearance_mode("System")  # Options: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue" (default), "green", "dark-blue"

class DownloadPanel(ctk.CTkFrame):
    def __init__(self, parent, user_id):
        super().__init__(parent, width=825, height=685)
        self.user_id = user_id

        # Database connection
        self.conn = sqlite3.connect('transactions.db')
        self.c = self.conn.cursor()

        # Configure grid layout for the main panel
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a main container frame with padding and rounded corners
        self.main_frame = ctk.CTkFrame(self, width=800, height=650, corner_radius=10)
        self.main_frame.pack(pady=15, padx=15, fill="both", expand=True)

        # Configure grid layout within the main frame
        self.main_frame.grid_rowconfigure(0, weight=0)  # Title
        self.main_frame.grid_rowconfigure(1, weight=0)  # Date Range
        self.main_frame.grid_rowconfigure(2, weight=0)  # Transaction Type
        self.main_frame.grid_rowconfigure(3, weight=0)  # Summary Option
        self.main_frame.grid_rowconfigure(4, weight=1)  # Download Buttons
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Download Transactions",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=(10, 20), padx=20)

        # Date Range Frame
        self.date_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.date_frame.grid(row=1, column=0, pady=(0, 20), padx=20, sticky="ew")
        self.date_frame.grid_columnconfigure(0, weight=0)
        self.date_frame.grid_columnconfigure(1, weight=1)
        self.date_frame.grid_columnconfigure(2, weight=1)

        self.label_date = ctk.CTkLabel(
            self.date_frame,
            text="Select Date Range:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.label_date.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        self.start_date = ctk.CTkEntry(
            self.date_frame,
            placeholder_text="Start Date (DD-MM-YYYY)",
            width=250
        )
        self.start_date.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="w")

        self.end_date = ctk.CTkEntry(
            self.date_frame,
            placeholder_text="End Date (DD-MM-YYYY)",
            width=250
        )
        self.end_date.grid(row=1, column=1, padx=(0, 10), pady=5, sticky="w")

        # Transaction Type Frame
        self.type_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.type_frame.grid(row=2, column=0, pady=(0, 20), padx=20, sticky="ew")
        self.type_frame.grid_columnconfigure(0, weight=0)
        self.type_frame.grid_columnconfigure(1, weight=1)

        self.label_type = ctk.CTkLabel(
            self.type_frame,
            text="Transaction Type:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.label_type.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        self.transaction_type = ctk.CTkOptionMenu(
            self.type_frame,
            values=["Both", "Credit (Deposit)", "Debit (Withdraw)"]
        )
        self.transaction_type.set("Both")
        self.transaction_type.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="w")

        # Summary Option Frame
        self.summary_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.summary_frame.grid(row=3, column=0, pady=(0, 20), padx=20, sticky="ew")
        self.summary_frame.grid_columnconfigure(0, weight=1)

        self.summary_check = ctk.CTkCheckBox(
            self.summary_frame,
            text="Include Summary Sheet (Only for Excel)",
            onvalue=1,
            offvalue=0
        )
        self.summary_check.grid(row=0, column=0, padx=0, pady=5, sticky="w")

        # Download Buttons Frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.grid(row=4, column=0, pady=(0, 20), padx=20, sticky="nsew")
        self.buttons_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.buttons_frame.grid_rowconfigure(0, weight=1)

        # Download Buttons
        self.download_excel_button = ctk.CTkButton(
            self.buttons_frame,
            text="Download as Excel",
            command=self.download_as_excel,
            width=180,
            height=40,
            fg_color="#4CAF50",  # Green color
            hover_color="#45A049"
        )
        self.download_excel_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.download_csv_button = ctk.CTkButton(
            self.buttons_frame,
            text="Download as CSV",
            command=self.download_as_csv,
            width=180,
            height=40,
            fg_color="#2196F3",  # Blue color
            hover_color="#1E88E5"
        )
        self.download_csv_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.download_tsv_button = ctk.CTkButton(
            self.buttons_frame,
            text="Download as TSV",
            command=self.download_as_tsv,
            width=180,
            height=40,
            fg_color="#FF9800",  # Orange color
            hover_color="#FB8C00"
        )
        self.download_tsv_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.download_zip_button = ctk.CTkButton(
            self.buttons_frame,
            text="Download as ZIP",
            command=self.download_as_zip,
            width=180,
            height=40,
            fg_color="#9C27B0",  # Purple color
            hover_color="#8E24AA"
        )
        self.download_zip_button.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

    def convert_date(self, date_str):
        """Convert date from dd-mm-yyyy to yyyy-mm-dd format."""
        try:
            return datetime.strptime(date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", f"Invalid date format: {date_str}. Please use DD-MM-YYYY.")
            return None

    def fetch_data(self):
        # Convert dates
        start_date = self.convert_date(self.start_date.get())
        end_date = self.convert_date(self.end_date.get())
        if not start_date or not end_date:
            return None, None

        # Build query based on transaction type
        type_filter = self.transaction_type.get()
        if type_filter == "Credit (Deposit)":
            query = "SELECT date, description, category, type, amount FROM transactions WHERE userid=? AND date BETWEEN ? AND ? AND type='deposit'"
        elif type_filter == "Debit (Withdraw)":
            query = "SELECT date, description, category, type, amount FROM transactions WHERE userid=? AND date BETWEEN ? AND ? AND type='withdraw'"
        else:
            query = "SELECT date, description, category, type, amount FROM transactions WHERE userid=? AND date BETWEEN ? AND ?"

        self.c.execute(query, (self.user_id, start_date, end_date))
        transactions = self.c.fetchall()

        if not transactions:
            messagebox.showinfo("Info", "No transactions found for the selected date range.")
            return None, None

        # Create DataFrame
        columns = ['Date', 'Description', 'Category', 'Type', 'Amount']
        df = pd.DataFrame(transactions, columns=columns)

        # Summary calculation for Excel downloads
        if self.summary_check.get() == 1 and 'Amount' in df:
            total_transactions = len(df)
            total_credit = df[df['Type'] == 'deposit']['Amount'].sum()
            total_debit = df[df['Type'] == 'withdraw']['Amount'].sum()
            net_amount = total_credit - total_debit
            summary = {
                'Total Transactions': total_transactions,
                'Total Credited': total_credit,
                'Total Debited': total_debit,
                'Net Amount': net_amount
            }
            return df, summary

        return df, None

    def download_as_excel(self):
        data, summary = self.fetch_data()
        if data is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Save as Excel"
        )
        if file_path:
            try:
                with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                    data.to_excel(writer, index=False, sheet_name="Transactions")

                    # Adding summary sheet
                    if summary:
                        summary_df = pd.DataFrame([summary])
                        summary_df.to_excel(writer, index=False, sheet_name="Summary")

                messagebox.showinfo("Success", "Excel file downloaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download Excel file: {e}")

    def download_as_csv(self):
        data, _ = self.fetch_data()
        if data is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save as CSV"
        )
        if file_path:
            try:
                data.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "CSV file downloaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download CSV file: {e}")

    def download_as_tsv(self):
        data, _ = self.fetch_data()
        if data is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".tsv",
            filetypes=[("TSV Files", "*.tsv")],
            title="Save as TSV"
        )
        if file_path:
            try:
                data.to_csv(file_path, index=False, sep='\t')
                messagebox.showinfo("Success", "TSV file downloaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download TSV file: {e}")

    def download_as_zip(self):
        data, summary = self.fetch_data()
        if data is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP Files", "*.zip")],
            title="Save as ZIP"
        )
        if file_path:
            try:
                with zipfile.ZipFile(file_path, 'w') as zipf:
                    temp_excel = "transactions.xlsx"
                    with pd.ExcelWriter(temp_excel, engine='xlsxwriter') as writer:
                        data.to_excel(writer, index=False, sheet_name="Transactions")

                        if summary:
                            summary_df = pd.DataFrame([summary])
                            summary_df.to_excel(writer, index=False, sheet_name="Summary")

                    zipf.write(temp_excel, arcname=os.path.basename(temp_excel))
                    os.remove(temp_excel)

                messagebox.showinfo("Success", "ZIP file downloaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download ZIP file: {e}")

# Sample usage
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Download Panel")
    root.geometry("825x685")
    root.resizable(False, False)  # Fixed window size

    # Simulating a logged-in user with a specific user_id
    download_panel = DownloadPanel(root, user_id=1)
    download_panel.pack(expand=True, fill="both")

    root.mainloop()
