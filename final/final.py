import customtkinter as ctk
from final.practise import LoginRegisterPanels
from final.practise2 import main_window

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(r"user_themes/Hades.json")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.iconbitmap(r"images/logo.ico")
        self.resizable(False, False)
        self.frame1()
        self.on_user_id_updated = self.frame2

    def frame1(self):
        self.login_app = LoginRegisterPanels(self)
        self.login_app.pack(expand=True, fill="both")

    def frame2(self, user_id):
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()
        self.main_frame = main_window(self,user_id)
        self.geometry("1000x700")
        self.withdraw()
        self.title("Finance Manager")
        self.main_frame.pack(expand=True, fill="both")
        self.deiconify()

    def go_to_login(self):
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()

        self.geometry("400x400")
        self.title("Login/Register")
        self.frame1()

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
