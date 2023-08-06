import tkinter
from tkinter import messagebox,filedialog
def showinfo(*args,show_only_info=True):
    if show_only_info:
        tk=tkinter.Tk()
        tk.withdraw()
    if args[0]:
        if not args[1]:
            messagebox.showinfo(args[0])
        else:
            messagebox.showinfo(args[0],args[1])
    else:
        messagebox.showinfo()
def askokcancel(*args,show_only_info=True):
    if show_only_info:
        tk=tkinter.Tk()
        tk.withdraw()
    if args[0]:
        if not args[1]:
            return messagebox.askokcancel(args[0])
        else:
            return messagebox.askokcancel(args[0],args[1])
    else:
        return messagebox.askokcancel()
def showwarning(*args,show_only_info=True):
    if show_only_info:
        tk=tkinter.Tk()
        tk.withdraw()
    if args[0]:
        if not args[1]:
            messagebox.showwarning(args[0])
        else:
            messagebox.showwarning(args[0],args[1])
    else:
        messagebox.showwarning()
def showerror(*args,show_only_info=True):
    if show_only_info:
        tk=tkinter.Tk()
        tk.withdraw()
    if args[0]:
        if not args[1]:
            messagebox.showerror(args[0])
        else:
            messagebox.showerror(args[0],args[1])
    else:
        messagebox.showerror()
def askyesnocancel(*args,show_only_info=True):
    if show_only_info:
        tk=tkinter.Tk()
        tk.withdraw()
    if args[0]:
        if not args[1]:
            return messagebox.askyesnocancel(args[0])
        else:
            return messagebox.askyesnocancel(args[0],args[1])
    else:
        return messagebox.askyesnocancel()
def askyesno(*args,show_only_info=False):
    if show_only_info:
        tk=tkinter.Tk()
        tk.withdraw()
    if args[0]:
        if not args[1]:
            return messagebox.askyesno(args[0])
        else:
            return messagebox.askyesno(args[0],args[1])
    else:
        return messagebox.askyesno()