import tkinter as tk
from tkinter import ttk
import sql_table
from user_parser import user_parser

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.view_records()

    def init_main(self):
        toolbar=tk.Frame(bg='#F5D4B3', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_dialog = tk.Button(toolbar, text='Добавить пользователя', command=self.open_dialig, bg='#F5BCB2', bd=0,
                                    compound=tk.TOP)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree=ttk.Treeview(self, columns=('id','name','description', 'n_followers'), height=15, show='headings')

        self.tree.column('id', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=150, anchor=tk.CENTER)
        self.tree.column('description', width=365, anchor=tk.CENTER)
        self.tree.column('n_followers', width=100, anchor=tk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Имя')
        self.tree.heading('description', text='Описание')
        self.tree.heading('n_followers', text='Кол-во подписчиков')

        self.tree.pack()

    def records(self, url):
        user_url = f'https://dzen.ru/{url}'
        user_parser(user_url)
        self.view_records()

    def view_records(self):
        element=sql_table.output_users()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row) for row in element]

    def open_dialig(self):
        Child()

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view=app
    def init_child(self):
        self.title('Добавить пользователя')
        self.geometry('400x220+400+300')
        self.resizable(False,False)

        Label_name = tk.Label(self, text='Ссылка:')
        Label_name.place(x=50,  y=50)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        btn_cancel=ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300,y=170)
        btn_ok=ttk.Button(self, text='Добавить')
        btn_ok.place(x=220, y=170)
        btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get()))

        self.grab_set()
        self.focus_set()

if  __name__=="__main__":
    root=tk.Tk()
    app=Main(root)
    app.pack()
    root.title("Parser")
    root.geometry("650x450+300+200")
    root.resizable(False,False)
    root.mainloop()