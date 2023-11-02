# ../pyw.exe 

# scripts_launcher.py

'''
Multi-login and Websites (plus Apps) automation.
'''

#######################################################
prg_tittle = '''Scripts, Apps, and Commands Launcher''' 
#######################################################
# author: Jorge Monti


# Built-in Libs
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msb
import os
from ctypes import windll


### Universal Vars'
tip = '''Just Press'''

### To resolve blurred tkinter text in some windows version
try:
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass    # To prevent possible crashes in different versions of operating systems


class ScrptLnch(tk.Tk):
    ''' Full tkinter Launcher App'''
    def __init__(self):
        super().__init__()
        self.title(prg_tittle)
        self.path = 'C:/Users/jm/git_repos/Password-Manager_w-Pandas/'
        self.pph_widgets()

    def pph_widgets(self):
        r, c, px, py = 0, 0, 10, 5

        label = ttk.Label(text='Passphrase:')
        label.grid(row=r, column=c, sticky=tk.W, padx=px, pady=py)
        self.pph_entry = tk.Entry(width=30, show='*')
        self.pph_entry.grid(row=r, column=c+1, sticky=tk.W, padx=px, pady=py)

        self.label2 = ttk.Label(text='Passphrase:')
        self.label2.grid(row=r+1, column=c, sticky=tk.W, padx=px, pady=py)
        self.pph2_entry = tk.Entry(width=30, show='*')
        self.pph2_entry.grid(row=r+1, column=c+1, sticky=tk.W, padx=px, pady=py)

        self.pph_btn = ttk.Button(self, text='OK', command=self.read_csd)
        self.pph_btn.grid(row=r+2, column=c+1, sticky=tk.S, padx=5, pady=5)

    def read_csd(self):
        try:
            self.__pph = self.pph_entry.get()
            pph2 = self.pph2_entry.get()
            assert self.__pph == pph2
        except Exception as e:
            self.__ext_prg(f'Critical Error getting Table: {e}')
        else:
            self.pph2_entry.delete(0, tk.END)   
            self.pph_btn.destroy()              # Delete pph_btn 'OK' button
            self.pph_entry.delete(0, tk.END)    # Clean passphrase field
            self.pph2_entry.destroy()             
            self.label2.destroy()
            self.main_widgets()                 # Build whole window (wo/table yet)
        return True
    
    def main_widgets(self):
        # Show tip Label
        self.instr_label = ttk.Label(self, text=tip)
        self.instr_label.grid(row=0, column=2, sticky=tk.N ,padx=10, pady=5)
        
        self.__mk_btn('realpython jp', self.realpython_jp, 1, 0)
        self.__mk_btn('reddit', self.reddit, 1, 1)  
        self.__mk_btn('Password Manager GUI', self.pmgui, 1, 2)
        self.__mk_btn('Password Manager TUI', self.pmtui, 2, 2)  
    
    def __mk_btn(self, txt, cmd, r, c):
        px, py, w = 10, 5, 20
        self.btn = ttk.Button(self, text=txt, command=cmd, width=w)
        self.btn.grid(row=r, column=c, sticky=tk.E, padx=px, pady=py)

    def pmgui(self):
        exe_str = f'pyw.exe {self.path}pmtk.pyw'
        self.__exec_cmd(exe_str)

    def pmtui(self):
        exe_str = f'python.exe {self.path}pmterm.py "{self.__pph}" '
        self.__exec_cmd(exe_str)

    def realpython_jp(self):
        self.__src_cnx('realpython jp')

    def reddit(self):
        self.__src_cnx('reddit')

    def __src_cnx(self, src):
        exe_str = f'python.exe {self.path}website_login.py "{src}" "{self.__pph}" '
        self.__exec_cmd(exe_str)

    def __exec_cmd(self, cmd):
        os.system(cmd)

    def __ext_prg(self, msg):
        msb.showerror('CRITICAL ERROR', msg)
        self.destroy()


if __name__ == "__main__":
    app = ScrptLnch()
    app.mainloop()