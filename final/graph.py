import customtkinter as ctk
from datetime import datetime
from tkcalendar import DateEntry
from final.database_control import get_transactions, get_sum_by_label
from CTkTable import *;
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from PIL import Image

class Graph(ctk.CTkTabview):
    def __init__(self, master, category_details, user_id, width=825, height=685):
        super().__init__(master, width=width, height=height)
        self.user_id = user_id
        self.today = datetime.today().date()
        self.labels = ['HOUSING', 'FOOD', 'TRANSPORT', 'UTILITIES', 'HEALTHCARE', 'PERSONAL', 'ENTERTAINMENT', 'EDUCATION', 'SAVINGS', 'MISCELLANEOUS']
        self.withdraw_data, self.deposit_data = get_sum_by_label(user_id=self.user_id, start_date=self.today, end_date=self.today, labels=self.labels)
        print(self.withdraw_data, self.deposit_data)
        self.category_details = category_details

        self.expenses_tab = self.add('Expenses')
        self.transactions_tab = self.add('Transactions')
        self.set("Expenses")

        self.render_expenses_tab()
        self.render_transactions_tab()

    def render_transactions_tab(self, start_date=datetime.today(), end_date=datetime.today()):
        frame = ctk.CTkFrame(self.transactions_tab)
        frame.pack(padx=20, pady=10, fill='x')

        # "From" label
        from_label = ctk.CTkLabel(frame, text="From:")
        from_label.pack(side='left', padx=(0, 10), anchor='w')

        #  "From" date entry
        from_date_entry = DateEntry(frame, background="darkblue", foreground="white", borderwidth=5, year=start_date.year, month=start_date.month, day=start_date.day, date_pattern='dd/MM/yyyy', font=('Arial', 12))
        from_date_entry.pack(side='left', padx=(0, 100))

        # "To" label
        to_label = ctk.CTkLabel(frame, text="To:")
        to_label.pack(side='left', padx=(100, 10))

        # "To" date entry
        to_date_entry = DateEntry(frame, background="darkblue", foreground="white", borderwidth=5, year=end_date.year, month=end_date.month, day=end_date.day, date_pattern='dd/MM/yyyy', font=('Arial', 12))
        to_date_entry.pack(side='left', padx=(0, 20))

        # Search button
        search_button = ctk.CTkButton(frame, text="Search", command=lambda: self.transactions_search_button_event(from_date_entry, to_date_entry))
        search_button.pack(side='right')

        self.render_transactions_details(from_date_entry, to_date_entry)
    
    def render_expenses_tab(self, start_date=datetime.today(), end_date=datetime.today()):
        # "From" label
        from_label = ctk.CTkLabel(self.expenses_tab, text="From:")
        from_label.place(relx=0.1, rely=0.03, anchor="center")

        # "From" date entry
        from_date_entry = DateEntry(self.expenses_tab, background="darkblue", foreground="white", borderwidth=5, year=start_date.year, month=start_date.month, day=start_date.day, date_pattern='dd/MM/yyyy', font=('Arial', 12))
        from_date_entry.place(relx=0.25, rely=0.03, anchor="center")

        # "To" label
        to_label = ctk.CTkLabel(self.expenses_tab, text="To:")
        to_label.place(relx=0.5, rely=0.03, anchor="center")

        # "To" date entry
        to_date_entry = DateEntry(self.expenses_tab, background="darkblue", foreground="white", borderwidth=5, year=end_date.year, month=end_date.month, day=end_date.day, date_pattern='dd/MM/yyyy', font=('Arial', 12))
        to_date_entry.place(relx=0.65, rely=0.03, anchor="center")

        # Search button
        search_button = ctk.CTkButton(self.expenses_tab, text="Search", command=lambda: self.expenses_search_button_event(from_date_entry, to_date_entry))
        search_button.place(relx=0.85, rely=0.03, anchor="center")

        self.graph_tabs = ctk.CTkTabview(self.expenses_tab, width=825, height=600)
        self.graph_tabs.place(relx=0.5, rely=0.6, anchor="center")

        self.withdraw_tab = self.graph_tabs.add('Withdraw')
        self.deposit_tab = self.graph_tabs.add('Deposit')
        self.graph_tabs.set('Withdraw')
        
        self.render_withdraw_tab_details()
        self.render_deposit_tab_details()

    def render_withdraw_tab_details(self):
        self.w_graph_frame = graph_frame(master=self.withdraw_tab, labels=self.labels, data=self.withdraw_data, corner_radius=10, width=824, height=400)
        self.w_graph_frame.place(relx=0.5, rely=0.3, anchor="center")

        self.w_category_frame = CategoriesFrame(self.withdraw_tab, data=self.withdraw_data, category_details=self.category_details, width=790, height=100, fg_color="white", corner_radius=10)
        self.w_category_frame.place(relx=0.5, rely=0.8, anchor="center")
    
    def render_deposit_tab_details(self):
        self.d_graph_frame = graph_frame(master=self.deposit_tab, labels=self.labels, data=self.deposit_data, corner_radius=10, width=824, height=400)
        self.d_graph_frame.place(relx=0.5, rely=0.3, anchor="center")

        self.d_category_frame = CategoriesFrame(self.deposit_tab, data=self.deposit_data, category_details=self.category_details, width=790, height=100, fg_color="white", corner_radius=10)
        self.d_category_frame.place(relx=0.5, rely=0.8, anchor="center")
    
    def transactions_search_button_event(self, from_date, to_date):
        print("called transactions")
        self.value = get_transactions(self.user_id, from_date.get_date(), to_date.get_date())
        self.table.configure(values=self.value)
    
    def expenses_search_button_event(self, from_date, to_date):
        start_date = from_date.get_date()
        end_date = to_date.get_date()
        print(start_date, end_date)

        self.w_graph_frame.data, self.d_graph_frame.data = get_sum_by_label(user_id=self.user_id, start_date=start_date, end_date=end_date, labels=self.labels)
        self.withdraw_data, self.deposit_data = get_sum_by_label(user_id=self.user_id, start_date=start_date, end_date=end_date, labels=self.labels)
        self.w_graph_frame.update_chart()
        self.d_graph_frame.update_chart()
        self.w_category_frame.update_data(self.withdraw_data)
        self.d_category_frame.update_data(self.deposit_data)
    
    def render_transactions_details(self, start_date, end_date):
        self.frame = ctk.CTkFrame(self.transactions_tab)
        self.scroll = ctk.CTkScrollableFrame(self.transactions_tab)

        self.value1 = [("DATE", "DESCRIPTION", "CATEGORY", "TYPE", "AMOUNT")]
        self.table1 = CTkTable(self.frame, row=1, column=5, values=self.value1, header_color="red", corner_radius=5, hover=False, wraplength=100)
        self.table1.pack(fill="both", expand=True)

        self.frame_height = self.table1.winfo_reqheight() + 20  
        self.frame.configure(height=self.frame_height)

        self.value = get_transactions(self.user_id, start_date.get_date(), end_date.get_date())
        self.table = CTkTable(master=self.scroll, row=100, column=5, values=self.value, corner_radius=5, hover=True, hover_color="gray", wraplength=100)
        self.table.pack(fill="both", expand=True)
        self.frame.pack(fill="x")
        self.scroll.pack(fill="both", expand=True)

class CategoriesFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, data, category_details, **kwargs):
        super().__init__(master, **kwargs)
        self.category_frames = []
        for i, details in enumerate(category_details):
            pady = (5, 30) if i == len(category_details) - 1 else 5
            frame = CategoryFrame(master=self, image=details["image"], amount=data[i], title=details["title"], border_color="black", border_width=5, fg_color="white")
            frame.pack(fill='x', pady=pady)
            self.category_frames.append(frame)

    def update_data(self, new_data):
        for frame, new_amount in zip(self.category_frames, new_data):
            frame.update_amount(new_amount)

class CategoryFrame(ctk.CTkFrame):
    def __init__(self, master, image, amount, title, **kwargs):
        super().__init__(master, **kwargs)
        
        self.image = ctk.CTkImage(dark_image=Image.open(image), size=(25, 25))
        self.amount = amount

        self.image_title_label = ctk.CTkLabel(self, image=self.image, text=title, text_color="black", compound="left", padx=15)
        self.image_title_label.pack(anchor="w", padx=10, pady=10, side="left")

        self.amount_label = ctk.CTkLabel(self, text=str(self.amount), text_color="black")
        self.amount_label.pack(anchor="e", padx=10, pady=10, side="right")

    def update_amount(self, new_amount):
        self.amount = new_amount
        self.amount_label.configure(text=str(self.amount))

class graph_frame(ctk.CTkFrame):
    def __init__(self, master, labels, data, width=824, height=400, *args, **kwargs):
        super().__init__(master, width=width, height=height, *args, **kwargs)
        self.labels = labels
        self.data = data

        self.render_expenses_details()

    def render_expenses_details(self):
        self.fig = Figure(figsize=(9, 4))
        self.ax = self.fig.add_subplot(111)
        self.fig.patch.set_facecolor('black')

        self.plot_types = ['Pie Chart', 'Bar Plot']
        self.plot_type_var = ctk.StringVar(value=self.plot_types[0])
        self.plot_menu = ctk.CTkOptionMenu(self, values=self.plot_types, variable=self.plot_type_var, command=self.update_chart, width=10)
        self.plot_menu.place(relx=0.88, rely=0.4)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.widget = self.canvas.get_tk_widget()
        self.widget.place(relx=0.01, rely=0.05)

        self.update_chart()

    def update_chart(self, event=None):
        plot_type = self.plot_type_var.get()
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_position([0.1, 0.1, 0.75, 0.75])

        if plot_type == 'Pie Chart':
            if all(value == 0 for value in self.data):
                self.ax.set_facecolor("black")
                self.ax.text(0.5, 0.5, 'NO DATA AVAILABLE', horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes, color="black", bbox=dict(facecolor="white", alpha=0.5))
            else:
                wedges, texts = self.ax.pie(self.data, shadow=True, radius=1.55, startangle=90)
                self.ax.legend(self.labels, loc="center left", bbox_to_anchor=(1.5, 0.5))

                self.annot = self.ax.annotate("", xy=(0, 0), xytext=(0,10), textcoords="offset points", ha="center", color="red", bbox=dict(boxstyle="round,pad=0.3", fc="black", ec="none", alpha=0.8))
                self.annot.set_visible(False)
                self.ax.set_aspect('equal')

                def update_annot_pie(wedge, index):
                    theta1, theta2 = wedge.theta1, wedge.theta2
                    center, radius = wedge.center, wedge.r
                    x = (radius * 0.7) * np.cos(np.deg2rad((theta1 + theta2) / 2)) + center[0]
                    y = (radius * 0.7) * np.sin(np.deg2rad((theta1 + theta2) / 2)) + center[1]
                    self.annot.xy = (x, y)
                    self.annot.set_text(f'{self.labels[index]}: {self.data[index]}')
                    self.annot.get_bbox_patch().set_alpha(0.8)

                def hover_pie(event):
                    vis = self.annot.get_visible()
                    if event.inaxes == self.ax:
                        for i, wedge in enumerate(wedges):
                            cont, _ = wedge.contains(event)
                            if cont:
                                update_annot_pie(wedge, i)
                                self.annot.set_visible(True)
                                self.fig.canvas.draw_idle()
                                return
                    if vis:
                        self.annot.set_visible(False)
                        self.fig.canvas.draw_idle()

                self.fig.canvas.mpl_connect("motion_notify_event", hover_pie)

        elif plot_type == 'Bar Plot':
            if all(value == 0 for value in self.data):
                self.ax.set_facecolor("black")
                self.ax.text(0.5, 0.5, 'NO DATA AVAILABLE', horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes, color="black", bbox=dict(facecolor="white", alpha=0.5))
            else:
                self.ax.set_facecolor('gray')
                self.bars = self.ax.bar(self.labels, self.data, color='skyblue')
                self.ax.set_xlabel('Categories', color="red")
                self.ax.set_ylabel('Amount', color="red")
                self.ax.tick_params(axis='both', colors="red")

                self.ax.set_xticks(range(len(self.labels)))
                self.ax.set_xticklabels(self.labels, rotation=45, ha='right')

                self.fig.subplots_adjust(bottom=0.25)

                self.annot = self.ax.annotate("", xy=(0, 0), xytext=(0, 10), textcoords="offset points", ha="center", color="white", bbox=dict(boxstyle="round, pad=0.3", fc="red", ec="none", alpha=0.8))
                self.annot.set_visible(False)

                def update_annot(bar):
                    x = bar.get_x() + bar.get_width() / 2
                    y = bar.get_height()
                    self.annot.xy = (x, y)
                    self.annot.set_text(f'{y:.2f}')
                    self.annot.get_bbox_patch().set_alpha(0.8)
        
                def hover(event):
                    vis = self.annot.get_visible()
                    if event.inaxes == self.ax:
                        for bar in self.bars:
                            cont, _ = bar.contains(event)
                            if cont:
                                update_annot(bar)
                                self.annot.set_visible(True)
                                self.fig.canvas.draw_idle()
                                return
                    if vis:
                        self.annot.set_visible(False)
                        self.fig.canvas.draw_idle()

                self.fig.canvas.mpl_connect("motion_notify_event", hover)

        self.canvas.draw()

# Create the main app window
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("865x685")  # Resized the window for better fit
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
        
        scrollable_frame = Graph(self, category_details, 1)
        scrollable_frame.pack()


# Run the application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Set theme
    app = App()
    app.mainloop()