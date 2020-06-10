import tkinter as tk
from tkinter import font  as tkfont
#import add_user

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenu, PageAdd, PageRemove, PageModify, PageTest):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Smart Ringbell", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        buttonAddUser = tk.Button(self, text="Aggiungi utente",
                            command=lambda: controller.show_frame("PageAdd"))
        buttonRemoveUser = tk.Button(self, text="Rimuovi utente",
                            command=lambda: controller.show_frame("PageRemove"))
        buttonModifyUser = tk.Button(self, text="Elimina utente",
                            command=lambda: controller.show_frame("PageModify"))
        buttonTest = tk.Button(self, text="Test",
                            command=lambda: controller.show_frame("PageTest"))
        buttonExit = tk.Button(self, text="Esci",
                            command=lambda: controller.show_frame("PageTwo"))
        buttonAddUser.pack()
        buttonRemoveUser.pack()
        buttonModifyUser.pack()
        buttonTest.pack()
        buttonExit.pack()


class PageAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Aggiungi Utente", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Ritorna al menu",
                           command=lambda: controller.show_frame("MainMenu"))
        button.pack()



class PageRemove(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Rimuovi utente", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Ritorna al menu",
                           command=lambda: controller.show_frame("MainMenu"))
        button.pack()

class PageModify(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Rimuovi utente", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Ritorna al menu",
                           command=lambda: controller.show_frame("MainMenu"))
        button.pack()

class PageTest(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Rimuovi utente", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Ritorna al menu",
                           command=lambda: controller.show_frame("MainMenu"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()