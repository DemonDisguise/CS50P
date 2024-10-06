import customtkinter as ctk
import sqlite3
import re
import hashlib  # Import hashlib for SHA-256 hashing
from email_validator import validate_email, EmailNotValidError
from tkinter import messagebox
from final.database_control import reset_transactions, reset_transactions_within_dates, delete_user_and_reset
from datetime import datetime

# Validator Class
class Validator:
    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email, check_deliverability=True)
            return True
        except EmailNotValidError:
            return False

    @staticmethod
    def validate_username(username):
        if len(username) < 5:
            return False  # Must be at least 5 characters long
        if not username[0].isalpha():
            return False  # Must not start with a special or numeric character
        return True

    @staticmethod
    def validate_password(password):
        password_regex = (
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$"
        )
        return bool(re.match(password_regex, password))


# Custom Password Dialog
class PasswordDialog(ctk.CTkToplevel):
    def __init__(self, master, title="Enter Password"):
        super().__init__(master)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)
        self.grab_set()  # Make the window modal

        self.password = None

        # Label
        label = ctk.CTkLabel(self, text="Please enter your current password:")
        label.pack(pady=10, padx=10)

        # Password Entry
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=5, padx=10, fill="x")
        self.password_entry.focus()

        # Buttons Frame
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=10)

        # OK Button
        ok_button = ctk.CTkButton(buttons_frame, text="OK", command=self.on_ok)
        ok_button.pack(side="left", padx=10)

        # Cancel Button
        cancel_button = ctk.CTkButton(buttons_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side="left", padx=10)

    def on_ok(self):
        self.password = self.password_entry.get()
        self.destroy()

    def on_cancel(self):
        self.password = None
        self.destroy()


# Custom Date Dialog
class CTkDateDialog(ctk.CTkToplevel):
    def __init__(self, master, title="Enter Date", prompt="Enter Date (dd-mm-yyyy):"):
        super().__init__(master)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)
        self.grab_set()  # Make the window modal

        self.date = None

        # Label
        label = ctk.CTkLabel(self, text=prompt)
        label.pack(pady=10, padx=10)

        # Date Entry
        self.date_entry = ctk.CTkEntry(self)
        self.date_entry.pack(pady=5, padx=10, fill="x")
        self.date_entry.focus()

        # Buttons Frame
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=10)

        # OK Button
        ok_button = ctk.CTkButton(buttons_frame, text="OK", command=self.on_ok)
        ok_button.pack(side="left", padx=10)

        # Cancel Button
        cancel_button = ctk.CTkButton(buttons_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side="left", padx=10)

    def on_ok(self):
        self.date = self.date_entry.get().strip()
        self.destroy()

    def on_cancel(self):
        self.date = None
        self.destroy()


# SettingsPanel Class
class SettingsPanel(ctk.CTkFrame):
    def __init__(self, master, userid, *args, **kwargs):
        super().__init__(master, width=825, height=685, *args, **kwargs)
        self.pack_propagate(False)  # Prevent frame from resizing to fit contents
        self.userid = userid

        # Initialize Database Connection
        self.conn = sqlite3.connect('transactions.db')
        self.c = self.conn.cursor()

        # Fetch Current User Information
        self.current_user = self.get_user_info()

        # Setup UI
        self.create_widgets()

    def get_user_info(self):
        self.c.execute("SELECT username, email, password FROM users WHERE userid = ?", (self.userid,))
        result = self.c.fetchone()
        if result:
            return {
                "username": result[0],
                "email": result[1],
                "password_hash": result[2]  # Store the hashed password for verification
            }
        else:
            messagebox.showerror("Error", "User not found.")
            self.master.destroy()

    def create_widgets(self):
        # Title Label
        title = ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)

        # Username Frame
        username_frame = ctk.CTkFrame(self)
        username_frame.pack(pady=10, padx=20, fill="x")
        username_label = ctk.CTkLabel(username_frame, text="Username:", width=100, anchor="w")
        username_label.pack(side="left", padx=(0, 10))
        self.username_entry = ctk.CTkEntry(username_frame, width=400)
        self.username_entry.insert(0, self.current_user["username"])
        self.username_entry.pack(side="left", fill="x", expand=True)

        # Email Frame
        email_frame = ctk.CTkFrame(self)
        email_frame.pack(pady=10, padx=20, fill="x")
        email_label = ctk.CTkLabel(email_frame, text="Email:", width=100, anchor="w")
        email_label.pack(side="left", padx=(0, 10))
        self.email_entry = ctk.CTkEntry(email_frame, width=400)
        self.email_entry.insert(0, self.current_user["email"])
        self.email_entry.pack(side="left", fill="x", expand=True)

        # Password Frame
        password_frame = ctk.CTkFrame(self)
        password_frame.pack(pady=10, padx=20, fill="x")
        password_label = ctk.CTkLabel(password_frame, text="New Password:", width=100, anchor="w")
        password_label.pack(side="left", padx=(0, 10))
        self.password_entry = ctk.CTkEntry(password_frame, width=400, show="*")
        self.password_entry.pack(side="left", fill="x", expand=True)

        # Confirm Password Frame
        confirm_password_frame = ctk.CTkFrame(self)
        confirm_password_frame.pack(pady=10, padx=20, fill="x")
        confirm_password_label = ctk.CTkLabel(confirm_password_frame, text="Confirm Password:", width=100, anchor="w")
        confirm_password_label.pack(side="left", padx=(0, 10))
        self.confirm_password_entry = ctk.CTkEntry(confirm_password_frame, width=400, show="*")
        self.confirm_password_entry.pack(side="left", fill="x", expand=True)

        # Delete Transactions Button
        delete_transactions_button = ctk.CTkButton(
            self, 
            text="Delete Transactions", 
            command=self.handle_delete_transactions,
            fg_color="red",  # Optional: Change color to indicate danger
            hover_color="darkred"
        )
        delete_transactions_button.pack(pady=10)

        # Delete Account Button
        delete_account_button = ctk.CTkButton(
            self,
            text="Delete Account",
            command=self.handle_delete_account,
            fg_color="red",
            hover_color="darkred"
        )
        delete_account_button.pack(pady=10)

        # Update Settings Button
        update_button = ctk.CTkButton(self, text="Update Settings", command=self.update_settings)
        update_button.pack(pady=30)

    def handle_delete_transactions(self):
        """Handle the deletion process by verifying password first."""
        if self.verify_current_password():
            self.open_delete_transactions_window()

    def verify_current_password(self):
        """Prompt the user to enter their current password and verify it."""
        password_dialog = PasswordDialog(self)
        self.wait_window(password_dialog)  # Wait until the dialog is closed

        entered_password = password_dialog.password

        if not entered_password:
            # User cancelled the dialog
            return False

        # Hash the entered password
        entered_password_hash = self.hash_password(entered_password)

        # Compare with stored password hash
        if entered_password_hash == self.current_user["password_hash"]:
            return True
        else:
            messagebox.showerror("Authentication Failed", "Incorrect password. Please try again.")
            return False

    def open_delete_transactions_window(self):
        """Open a CTkTopLevel window with options to delete transactions."""
        delete_window = ctk.CTkToplevel(self)
        delete_window.geometry("400x300")
        delete_window.title("Delete Transactions")
        delete_window.grab_set()  # Make the window modal

        # Title Label
        label = ctk.CTkLabel(delete_window, text="Choose an option to delete transactions:", font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(pady=20, padx=20)

        # Clear All Transactions Button
        clear_all_button = ctk.CTkButton(
            delete_window, 
            text="Clear All Transactions", 
            command=lambda: self.confirm_clear_all_transactions(delete_window),
            fg_color="red",
            hover_color="darkred"
        )
        clear_all_button.pack(pady=10, padx=20, fill="x")

        # Clear Transactions By Date Button
        clear_by_date_button = ctk.CTkButton(
            delete_window, 
            text="Clear Transactions By Date", 
            command=lambda: self.handle_clear_transactions_by_date(delete_window)
        )
        clear_by_date_button.pack(pady=10, padx=20, fill="x")

    def confirm_clear_all_transactions(self, parent_window):
        """Ask for confirmation and clear all transactions for the user."""
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all your transactions?", parent=parent_window)
        if confirm:
            try:
                reset_transactions(self.userid)
                messagebox.showinfo("Success", "All transactions deleted successfully.", parent=parent_window)
                parent_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}", parent=parent_window)

    def handle_clear_transactions_by_date(self, parent_window):
        """Handle the process of clearing transactions by date."""
        # Prompt for From Date
        from_date = self.prompt_for_date("From Date", parent_window)
        if not from_date:
            return  # User cancelled or invalid input

        # Prompt for To Date
        to_date = self.prompt_for_date("To Date", parent_window)
        if not to_date:
            return  # User cancelled or invalid input

        # Ensure From Date is not after To Date
        if from_date > to_date:
            messagebox.showerror("Invalid Date Range", "From Date cannot be after To Date.", parent=parent_window)
            return

        # Confirm Deletion
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete transactions from {from_date.strftime('%d-%m-%Y')} to {to_date.strftime('%d-%m-%Y')}?",
            parent=parent_window
        )
        if confirm:
            try:
                # Convert dates to yyyy-mm-dd format
                from_date_str = from_date.strftime('%Y-%m-%d')
                to_date_str = to_date.strftime('%Y-%m-%d')
                reset_transactions_within_dates(self.userid, from_date_str, to_date_str)
                messagebox.showinfo("Success", "Selected transactions deleted successfully.", parent=parent_window)
                parent_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}", parent=parent_window)

    def prompt_for_date(self, date_type, parent_window):
        """Prompt the user to enter a date and validate its format."""
        dialog = CTkDateDialog(self, title=f"Enter {date_type}", prompt=f"Enter {date_type} (dd-mm-yyyy):")
        self.wait_window(dialog)

        date_input = dialog.date

        if not date_input:
            # User cancelled the dialog
            return None

        # Validate and parse the date
        try:
            # Parse the date with dd-mm-yyyy format
            date_obj = datetime.strptime(date_input, '%d-%m-%Y')
            return date_obj
        except ValueError:
            messagebox.showerror("Invalid Date", f"{date_type} is not a valid date or not in the correct format (dd-mm-yyyy).", parent=parent_window)
            return None

    def hash_password(self, password):
        """Hashes the password using SHA-256 and returns the hexadecimal digest."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def update_settings(self):
        new_username = self.username_entry.get().strip()
        new_email = self.email_entry.get().strip()
        new_password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validation Flags
        valid = True
        errors = []

        # Validate Username
        if new_username != self.current_user["username"]:
            if not Validator.validate_username(new_username):
                valid = False
                errors.append("Invalid Username: Must be at least 5 characters long and start with a letter.")
            else:
                # Check if username is taken
                self.c.execute("SELECT userid FROM users WHERE username = ?", (new_username,))
                if self.c.fetchone():
                    valid = False
                    errors.append("Username is already taken.")

        # Validate Email
        if new_email != self.current_user["email"]:
            if not Validator.validate_email_address(new_email):
                valid = False
                errors.append("Invalid Email Address.")
            else:
                # Check if email is taken
                self.c.execute("SELECT userid FROM users WHERE email = ?", (new_email,))
                if self.c.fetchone():
                    valid = False
                    errors.append("Email is already in use.")

        # Validate Password (only if user wants to change it)
        if new_password or confirm_password:
            if new_password != confirm_password:
                valid = False
                errors.append("Passwords do not match.")
            elif not Validator.validate_password(new_password):
                valid = False
                errors.append("Invalid Password: Must be at least 8 characters long, include uppercase and lowercase letters, a number, and a special character.")

        if not valid:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        # Prepare Update Statements
        update_fields = []
        params = []

        if new_username != self.current_user["username"]:
            update_fields.append("username = ?")
            params.append(new_username)

        if new_email != self.current_user["email"]:
            update_fields.append("email = ?")
            params.append(new_email)

        if new_password:
            hashed_password = self.hash_password(new_password)
            update_fields.append("password = ?")
            params.append(hashed_password)

        if update_fields:
            params.append(self.userid)
            update_query = f"UPDATE users SET {', '.join(update_fields)} WHERE userid = ?"
            try:
                self.c.execute(update_query, tuple(params))
                self.conn.commit()
                messagebox.showinfo("Success", "Settings updated successfully.")
                # Update current_user dictionary
                if new_username != self.current_user["username"]:
                    self.current_user["username"] = new_username
                if new_email != self.current_user["email"]:
                    self.current_user["email"] = new_email
                if new_password:
                    self.current_user["password_hash"] = self.hash_password(new_password)
                # Clear password fields
                self.password_entry.delete(0, 'end')
                self.confirm_password_entry.delete(0, 'end')
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
        else:
            messagebox.showinfo("No Changes", "No changes were made.")

    def handle_delete_account(self):
        """Handle the account deletion process by verifying password first."""
        if self.verify_current_password():
            self.confirm_delete_account()

    def confirm_delete_account(self):
        """Ask for confirmation and delete the user account."""
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete your account? This action cannot be undone.")
        if confirm:
            try:
                delete_user_and_reset(self.userid)
                messagebox.showinfo("Account Deleted", "Your account has been deleted successfully.")
                self.master.destroy()  # Close the application
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while deleting your account: {e}")

    def on_close(self):
        self.conn.close()
        self.master.destroy()


# Example Usage
if __name__ == "__main__":
    import sys

    # Example user ID. In a real application, you'd obtain this after user login.
    CURRENT_USER_ID = 1

    # Initialize CustomTkinter appearance (optional)
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

    app = ctk.CTk()
    app.geometry("825x685")
    app.title("Finance Manager - Settings")

    settings_panel = SettingsPanel(app, CURRENT_USER_ID)
    settings_panel.pack(fill="both", expand=True)

    app.protocol("WM_DELETE_WINDOW", settings_panel.on_close)
    app.mainloop()
