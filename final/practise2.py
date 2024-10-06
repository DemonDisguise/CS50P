import customtkinter as ctk
from datetime import datetime
from PIL import Image
from final.database_control import update_balance
from final.download import DownloadPanel
from final.settings import SettingsPanel
from final.transactions import Transactions
from final.graph import Graph
import tkinter as tk

class main_window(ctk.CTkFrame):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.width = 1000
        self.height = 700

        self.user_id = user_id

        self.category_details = [
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

        # navigation
        self.navigation_panel = ctk.CTkFrame(self, width=150, height=690)
        self.navigation_panel.place(relx=0.01, rely=0.5, anchor="w")
        self.render_navigation_panel()

        self.current_frame = None

        # details
        self.details_panel = ctk.CTkFrame(self, width=830, height=690)
        self.details_panel.place(relx=0.168, rely=0.5, anchor="w")
        update_balance(self)

        self.render_details()
    
    def switch_frame(self, new_frame):
        if self.current_frame:
            self.current_frame.place_forget()
        self.current_frame = new_frame
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    def render_download_panel(self):
        self.download_panel = DownloadPanel(self.details_panel, user_id=self.user_id)
        self.switch_frame(self.download_panel)
    
    def render_settings_panel(self):
        self.settings_panel = SettingsPanel(self.details_panel, self.user_id)
        self.switch_frame(self.settings_panel)

    def render_home_panel(self):
        self.switch_frame(self.type_of_detail_tabview)
    
    def add_button_event(self):
        self.transactions_panel = Transactions(self, self.details_panel, userid=self.user_id, category_details=self.category_details)
        self.switch_frame(self.transactions_panel)
    
    def render_navigation_panel(self):
        # navigation buttons
        # total balance
        self.balance_panel = ctk.CTkFrame(self.navigation_panel, height=100, width=148)
        self.balance_panel.place(relx=0.5, rely=0.1, anchor="center")

        self.balance_label = ctk.CTkLabel(self.balance_panel, text="Balance", width=145, height=48)
        self.balance_label.pack(fill="x")

        self.amount_label = ctk.CTkLabel(self.balance_panel, width=145, height=48, anchor='w', font=('Arial', 15))

        Tooltip(self.amount_label, "K = Thousand, L = Lakh, Cr = Crore")
        self.amount_label.pack(fill='x')

        self.home_button = ctk.CTkButton(self.navigation_panel, text="Home", command= self.render_home_panel)
        self.home_button.place(relx=0.5, rely=0.4, anchor="center")

        self.download_button = ctk.CTkButton(self.navigation_panel, text="Download", command= self.render_download_panel)
        self.download_button.place(relx=0.5, rely=0.5, anchor="center")

        self.account_button = ctk.CTkButton(self.navigation_panel, text="Settings", command= self.render_settings_panel)
        self.account_button.place(relx=0.5, rely=0.6, anchor="center")

        self.logout_button = ctk.CTkButton(self.navigation_panel, text="Logout", command= self.master.go_to_login)
        self.logout_button.place(relx=0.5, rely=0.7, anchor="center")

        self.add_button = ctk.CTkButton(self.navigation_panel, width=60, height=60, text=None, image=ctk.CTkImage(Image.open(r"./images/add.png"), size=(50, 50)), command=self.add_button_event, corner_radius=20)
        self.add_button.place(relx=0.5, rely=0.9, anchor="center")

    def render_details(self):
        self.type_of_detail_tabview = Graph(self.details_panel, category_details=self.category_details, user_id=self.user_id)
        self.switch_frame(self.type_of_detail_tabview)

class Tooltip:
    """
    Creates a tooltip for a given widget.
    """
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Motion>", self.move_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x = event.x_root + 20
        y = event.y_root + 10
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove window decorations
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("Arial", "10", "normal"))
        label.pack(ipadx=1)

    def move_tooltip(self, event):
        if self.tooltip_window:
            x = event.x_root + 20
            y = event.y_root + 10
            self.tooltip_window.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self, event=None):
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()


def main():

    a = main_window(user_id=1)
    a.mainloop()


if __name__ == "__main__":
    main()