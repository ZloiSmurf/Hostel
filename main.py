import db_connect as db
from admin_window import AdminWindow
from login_page import *
from User import User

class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.title("Hotel")
        self.geometry('720x600')
        self.frames = {}

        #for F in (Login, Registration, GuestAccount):
        frame = Login(self.container, self, DB, current_user)
        self.frames[Login] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        frame = Registration(self.container, self, DB)
        self.frames[Registration] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_guest_account(self, cur_user):
        frame = GuestAccount(self.container, self, DB, cur_user)
        self.frames[GuestAccount] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(GuestAccount)

    def show_admin_account(self, cur_user):
        frame = AdminWindow(self.container, self, DB, cur_user)
        self.frames[AdminWindow] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(AdminWindow)


if __name__ == "__main__":
    DB = db.DataBase()
    current_user = User()
    app = Main()
    app.mainloop()
