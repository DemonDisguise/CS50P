import customtkinter as ctk
from tkinter import messagebox
from email_validator import validate_email, EmailNotValidError
import re
from final.database_control import add_user, get_usernames, verify_user, get_userid
from final.practise2 import main_window


class LoginRegisterPanels(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.width = 400
        self.height = 400
        self.render_login_panel()
        self.user_id = 0

    def login_event(self):
        self.username = self.login_user_name_entry.get()
        self.password = self.login_password_entry.get()

        self.verification_result = verify_user(self.username, self.password)
        if self.verification_result == "Success":
            self.user_id = get_userid(self.username)
            self.destroy()
            self.notify_user_id_updated()
        elif self.verification_result == "IncorrectPassword":
            messagebox.showerror(title="Error", message="Wrong Password")
        else:
            messagebox.showwarning(
                title="Error",
                message="Username not found, recheck or register if not registered",
            )

    def notify_user_id_updated(self):
        if hasattr(self.master, "on_user_id_updated"):
            self.master.on_user_id_updated(self.user_id)

    def password_visibility(self):
        if self.check_var_pass.get() == "on":
            self.login_password_entry.configure(show="")
        else:
            self.login_password_entry.configure(show="•")

    def sign_up_event(self):
        self.login_panel.place_forget()
        self.login_panel.destroy()
        self.render_register_panel()

    def on_enter(self, event):
        self.sign_up_button.configure(font=("Arial", 15, "underline"))

    def on_leave(self, event):
        self.sign_up_button.configure(font=("Arial", 15))

    def render_login_panel(self):
        self.master.title("Login Page")
        self.login_panel = ctk.CTkFrame(self)
        self.login_panel.place(relwidth=1, relheight=1)

        # Username
        self.login_user_name_label = ctk.CTkLabel(self.login_panel, text="Username")
        self.login_user_name_label.place(relx=0.2, rely=0.2, anchor="center")

        self.login_user_name_entry = ctk.CTkEntry(
            self.login_panel,
            placeholder_text="Username",
            placeholder_text_color="green",
            width=200,
            height=35,
            corner_radius=10,
        )
        self.login_user_name_entry.place(relx=0.6, rely=0.2, anchor="center")

        # Password
        self.login_password_label = ctk.CTkLabel(self.login_panel, text="Password")
        self.login_password_label.place(relx=0.2, rely=0.4, anchor="center")

        self.login_password_entry = ctk.CTkEntry(
            self.login_panel,
            placeholder_text="Password",
            placeholder_text_color="green",
            show="•",
            width=200,
            height=35,
            border_width=2,
            corner_radius=10,
        )
        self.login_password_entry.place(relx=0.6, rely=0.4, anchor="center")

        # show password
        self.check_var_pass = ctk.StringVar()
        self.password_visibility_checkbox = ctk.CTkCheckBox(
            self.login_panel,
            text="Show Password",
            variable=self.check_var_pass,
            onvalue="on",
            offvalue="off",
            command=self.password_visibility,
        )
        self.password_visibility_checkbox.place(relx=0.5, rely=0.5, anchor="center")

        self.sign_up_button = ctk.CTkButton(
            self.login_panel,
            font=("Arial", 15),
            text="Sign up",
            command=self.sign_up_event,
            fg_color="transparent",
            hover=False,
            width=30,
            height=30,
        )
        self.sign_up_button.place(relx=0.5, rely=0.7, anchor="center")

        self.sign_up_button.bind("<Enter>", self.on_enter)
        self.sign_up_button.bind("<Leave>", self.on_leave)

        self.login_button = ctk.CTkButton(
            self.login_panel, text="login", command=lambda: self.login_event()
        )
        self.login_button.place(relx=0.5, rely=0.8, anchor="center")
        print("Login successfull")

    def register_event(self):
        username = self.register_user_name_entry.get().strip()
        email = self.register_email_entry.get().strip()
        password = self.register_password_entry.get().strip()

        email_valid = Test.validate_mail(email)
        username_valid = Test.validate_username(username)
        password_valid = Test.validate_password(password)

        if email_valid and username_valid and password_valid:
            add_user(username, email, password)

            self.register_label = ctk.CTkLabel(
                self.register_panel, text="Registered", text_color="green"
            )
            self.register_label.place(relx=0.5, rely=0.8, anchor="center")

            self.register_panel.after(5000, lambda: self.switch_panels("login_panel"))
        else:
            if not email_valid:
                messagebox.showerror(title="Error", message="Invalid email")
            if not username_valid:
                messagebox.showerror(
                    title="Invalid username",
                    message="Your username should contain\n• It should be atleast be 5 characters long\n• It should not start with special or numeric character",
                )
            if not password_valid:
                messagebox.showerror(
                    title="Invalid password",
                    message="Password should contain:\n• atleast 8 characters\n• Include both uppercase and lowercase characters\n• Include digits\n• Allowed special characters !@#$%^&*\nAvoid using easily guessable information.",
                )

    def render_register_panel(self):
        self.master.title("Register Page")
        self.register_panel = ctk.CTkFrame(self)
        self.register_panel.place(relwidth=1, relheight=1)

        # Email
        self.register_email = ctk.CTkLabel(self.register_panel, text="Set Email")
        self.register_email.place(relx=0.2, rely=0.2, anchor="center")

        self.register_email_entry = ctk.CTkEntry(
            self.register_panel,
            placeholder_text="Email",
            placeholder_text_color="white",
            width=200,
            height=35,
            border_width=2,
            corner_radius=10,
        )
        self.register_email_entry.place(relx=0.6, rely=0.2, anchor="center")

        # Username
        self.register_user_name_label = ctk.CTkLabel(
            self.register_panel, text="Set Username"
        )
        self.register_user_name_label.place(relx=0.2, rely=0.4, anchor="center")

        self.register_user_name_entry = ctk.CTkEntry(
            self.register_panel,
            placeholder_text="Username",
            placeholder_text_color="white",
            width=200,
            height=35,
            border_width=2,
            corner_radius=10,
        )
        self.register_user_name_entry.place(relx=0.6, rely=0.4, anchor="center")

        # Password
        self.register_password = ctk.CTkLabel(self.register_panel, text="Set Password")
        self.register_password.place(relx=0.2, rely=0.6, anchor="center")

        self.register_password_entry = ctk.CTkEntry(
            self.register_panel,
            placeholder_text="Password",
            placeholder_text_color="white",
            width=200,
            height=35,
            border_width=2,
            corner_radius=10,
        )
        self.register_password_entry.place(relx=0.6, rely=0.6, anchor="center")

        self.register_button = ctk.CTkButton(
            self.register_panel, text="register", command=lambda: self.register_event()
        )
        self.register_button.place(relx=0.5, rely=0.9, anchor="center")

        print("register successfull")

    def switch_panels(self, panel):
        if panel == "login_panel":
            self.register_panel.place_forget()
            self.register_panel.destroy()
            self.render_login_panel()
        elif panel == "register_panel":
            self.login_panel.place_forget()
            self.login_panel.destroy()
            self.render_register_panel()

class Test:
    @staticmethod
    def validate_mail(email):
        try:
            validate_email(email, check_deliverability=True)
            return True
        except EmailNotValidError:
            return False

    @staticmethod
    def validate_username(username):
        usernames = get_usernames()  # You'll need to implement this function
        if username in usernames:
            return False
        else:
            pattern = r"^[A-Za-z][\w\W]{3,}$"
            return bool(re.match(pattern, username))

    @staticmethod
    def validate_password(password):
        password_regex = (
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$"
        )
        return bool(re.match(password_regex, password))

def main():
    app = ctk.CTk()
    app.geometry("400x400")

    login_app = LoginRegisterPanels(app)
    login_app.pack(expand=True, fill="both")
    app.mainloop()
    user_id = login_app.user_id
    print(user_id)


if __name__ == "__main__":
    main()
