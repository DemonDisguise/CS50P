import customtkinter as ctk
from PIL import Image
import re
from datetime import datetime
from CTkMessagebox import CTkMessagebox
from final.database_control import add_transactions, update_balance

class Transactions(ctk.CTkScrollableFrame):
    def __init__(self, master, parent, userid, category_details, *args, **kwargs):
        super().__init__(parent, width=825, height=685, *args, **kwargs)
        self.master = master
        self.userid = userid
        self.selected_button = None
        self.selected_category = "MISCELLANEOUS"  # Set default category to MISCELLANEOUS
        self.image_objs = []  # Store image objects to prevent garbage collection
        self.category_details = category_details
        
        # Call method to create the grid
        self.create_grid()
        
        # Add transaction type panel
        self.add_transaction_type_panel()
        
        # Add input panel for date, description, and amount
        self.add_input_panel()
        
        # Add button to add transaction
        self.add_transaction_button()

    def create_grid(self):
        """Creates a grid of images and titles"""
        title_label = ctk.CTkLabel(self, text="Select Category", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=5, padx=10, pady=(20, 10))

        for index, category in enumerate(self.category_details):
            # Load image and resize using CTkImage
            image = ctk.CTkImage(Image.open(category['image']), size=(80, 80))  # Slightly smaller images
            self.image_objs.append(image)  # Keep a reference to avoid garbage collection

            # Create a button for each image and title
            button = ctk.CTkButton(self, image=image, text=category['title'], 
                                   compound="top", fg_color="gray", hover_color="lightblue",
                                   command=lambda i=index: self.on_image_selected(i))
            button.grid(row=(index // 5) + 1, column=index % 5, padx=10, pady=10)  # Arrange buttons in a grid

            # Set the "Miscellaneous" category as the default selected button
            if category['title'] == "MISCELLANEOUS":
                self.selected_button = button
                self.selected_button.configure(fg_color="green")

                # Ensure the internal selection matches the default "Miscellaneous"
                self.selected_category = "MISCELLANEOUS"

    def add_transaction_type_panel(self):
        """Adds a panel for selecting Transaction Type (Withdraw/Deposit)"""
        type_frame = ctk.CTkFrame(self)
        type_frame.grid(row=3, column=0, columnspan=5, pady=20, padx=10, sticky="nsew")

        transaction_type_label = ctk.CTkLabel(type_frame, text="Transaction Type", font=("Arial", 18, "bold"))
        transaction_type_label.pack(pady=(10, 5))

        # Radio buttons for "Withdraw" and "Deposit"
        self.transaction_type = ctk.StringVar(value="withdraw")

        withdraw_radio = ctk.CTkRadioButton(type_frame, text="Withdraw", variable=self.transaction_type, value="withdraw")
        withdraw_radio.pack(side="left", padx=10, pady=10)

        deposit_radio = ctk.CTkRadioButton(type_frame, text="Deposit", variable=self.transaction_type, value="deposit")
        deposit_radio.pack(side="left", padx=10, pady=10)

    def add_input_panel(self):
        """Adds a panel for inputting date, description, and amount"""
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=4, column=0, columnspan=5, pady=20, padx=10, sticky="nsew")

        input_label = ctk.CTkLabel(input_frame, text="Transaction Details", font=("Arial", 18, "bold"))
        input_label.pack(pady=(10, 5))

        # Entry for date
        self.date_entry = ctk.CTkEntry(input_frame, placeholder_text="Date (dd-mm-yyyy)", width=250)
        self.date_entry.pack(pady=5)

        # Entry for description
        self.description_entry = ctk.CTkEntry(input_frame, placeholder_text="Description", width=250)
        self.description_entry.pack(pady=5)

        # Entry for amount
        self.amount_entry = ctk.CTkEntry(input_frame, placeholder_text="Amount", width=250)
        self.amount_entry.pack(pady=5)

    def add_transaction_button(self):
        """Adds a button to add the transaction"""
        add_button = ctk.CTkButton(self, text="Add Transaction", command=self.get_transactions)
        add_button.grid(row=5, column=0, columnspan=5, pady=20)

    def on_image_selected(self, index):
        """Callback for when an image is selected"""
        # Deselect the previously selected button
        if self.selected_button is not None:
            self.selected_button.configure(fg_color="gray")

        # Select the new button
        selected_category = self.category_details[index]
        print(f"Selected Category: {selected_category['title']}")  # Print selected category for reference

        # Get the button widget that was clicked
        self.selected_button = self.winfo_children()[index + 1]
        self.selected_button.configure(fg_color="green")

        # Set the selected category internally
        self.selected_category = selected_category['title']

    def get_transactions(self):
        """Handles adding the transaction and validating input"""
        # Validate date
        date_input = self.date_entry.get()
        normalized_date = self.normalize_date(date_input)
        if not self.validate_date(normalized_date):
            CTkMessagebox(title="Invalid Date", message="Please enter the date in the format dd-mm-yyyy.", icon="warning")
            self.date_entry.delete(0, ctk.END)
            return

        # Validate amount
        amount_input = self.amount_entry.get()
        if not self.validate_amount(amount_input):
            CTkMessagebox(title="Invalid Amount", message="Please enter a valid amount.", icon="warning")
            self.amount_entry.delete(0, ctk.END)
            return

        # Get the transaction type
        transaction_type = self.transaction_type.get()
        
        # Gather all data, using "MISCELLANEOUS" as default if no button selected
        selected_category = getattr(self, 'selected_category', "MISCELLANEOUS")
        
        transaction_data = {
            "category": selected_category,
            "transaction_type": transaction_type,
            "date": self.convert_date_format(normalized_date),
            "description": self.description_entry.get(),
            "amount": float(amount_input)
        }

        add_transactions(self.userid, transaction_data['date'], transaction_data['description'], transaction_data['category'], transaction_data['transaction_type'], transaction_data['amount'])

        update_balance(self.master)

        CTkMessagebox(title="Transaction added", message="Transaction added successfully.", icon="check")

    def validate_date(self, date_str):
        """Validates the date format dd-mm-yyyy"""
        regex = r'^\d{2}-\d{2}-\d{4}$'
        return re.match(regex, date_str) is not None

    def normalize_date(self, date_str):
        """Normalizes the date to dd-mm-yyyy format"""
        parts = date_str.split('-')
        if len(parts) != 3:
            return date_str  # Return original if not valid
        
        day, month, year = parts[0].zfill(2), parts[1].zfill(2), parts[2]
        return f"{day}-{month}-{year}"

    def validate_amount(self, amount_str):
        """Validates the amount is a valid number"""
        try:
            if amount_str.strip() == "" or float(amount_str) <= 0:
                return False
            return True
        except ValueError:
            return False

    def convert_date_format(self, date_str):
        """Converts date from dd-mm-yyyy to yyyy-mm-dd"""
        day, month, year = date_str.split('-')
        return f"{year}-{month}-{day}"


# Create the main app window
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("850x800")  # Resized the window for better fit
        self.title("Add Transactions")

        category_details = [
            {"image": r'./images/home.png', "title": "HOUSING"},
            {"image": r'./images/fast-food.png', "title": "FOOD"},
            {"image": r'./images/public-transport.png', "title": "TRANSPORT"},
            {"image": r'./images/subscriptions.png', "title": "UTILITIES"},
            {"image": r'./images/first-aid-kit.png', "title": "HEALTHCARE"},
            {"image": r'./images/user.png', "title": "PERSONAL"},
            {"image": r'./images/watching-a-movie.png', "title": "ENTERTAINMENT"},
            {"image": r'./images/mortarboard.png', "title": "EDUCATION"},
            {"image": r'./images/piggy-bank.png', "title": "SAVINGS"},
            {"image": r'./images/price.png', "title": "MISCELLANEOUS"},
        ]
        
        scrollable_frame = Transactions(self, userid=1, category_details=category_details)
        scrollable_frame.pack(padx=10, pady=10)


# Run the application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Set theme
    app = App()
    app.mainloop()

