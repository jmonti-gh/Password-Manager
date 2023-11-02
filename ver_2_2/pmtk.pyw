# !... pyw.exe pmtk.pyw

# pmtk.pyw

'''
GUI Password Manager
'''


#######################################################
prg_tittle = ''' Password Manager -tkinter- v. 2.2''' 
#######################################################
# author: Jorge Monti


# Built-in Libs
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msb
import itertools
from ctypes import windll

# Other Libs
from pandastable import Table

# Own module
import pmcore as pmc


### Universal Vars'
tip = '''| Add Password |\t> Fill at least Service, Username, and 
        Password fields to add a new Service.'''

### TO-DO future read the help from a json or a txt or an exce, csv... xml ¡?¡?¡?
help = '''
| Add Password |  > Fill at least Service, Username, and Password fields to add a new Service/Password.\n
| Get Password |  > To view the password, enter the name of the Service.\n
| Get Table |  > To view the current status of the Service Table.\n
| Get User |  > To view user enter Service name. \n
| Change Password |  > Fill Service name and both Password fields to change the password.\n
| Change URL |  > Fill Service name and URL fields to change the URL.\n
| Updates Notes |  > Fill Service name and Notes fields to change the URL.\n
| Ser Next Pwd |  > Fill Service name and both next_pwd fields to change the password.\n
| Service Search |  > Enter part of the Service name (ignores case).\n
| Delete Service |  > Enter Service name - It's NOT possible to Undelete.\n
| Table by Service |  > Get the table of services sorted alphabetically.\n
| Tbl Ignoring Case |  > Get the table of services sorted alphabetically ignoring case.\n
| Full Monti |  > Show all columns and rows of the Service Table. Need Passphrase. (Entire Table).
'''

### To resolve blurred tkinter text in some windows version
try:
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass    # To prevent possible crashes in different versions of operating systems


class ShowDF(tk.Frame):
    ''' Very Basic DF display in a table using pandastable library'''
    def __init__(self, df):
        tk.Frame.__init__(self)
        f = tk.Frame(self.master)
        f.grid(row=10, columnspan=4, pady=10, sticky='nsew')
        pt = Table(f, dataframe=df, showstatusbar=True)
        pt.editable = False
        pt.show()


class PwdMgr(tk.Tk):
    ''' Full tkinter Password Manager App'''
    def __init__(self):
        super().__init__()
        self.title(prg_tittle)
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.pph_widgets()
        self.bind("<Control-m>", lambda event: self.__ctrl_m())     # Secret keystroke

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
            self.pmt = pmc.PmTable(self.__pph)
        except Exception as e:
            self.__ext_prg(f'Critical Error getting Table: {e}')
        else:
            # get columns names as independent vars
            self.s, self.u, self.p, self.r, self.d, self.n, self.np, self.nd = self.pmt.get_cols()
            self.pph2_entry.delete(0, tk.END)   
            self.pph_btn.destroy()              # Delete pph_btn 'OK' button
            self.pph_entry.delete(0, tk.END)    # Clean passphrase field
            self.pph2_entry.destroy()             
            self.label2.destroy()
            self.main_widgets()                 # Build whole window (wo/table yet)
        return True
    
    def main_widgets(self):
        # Show Instructions Label
        self.instr_label = ttk.Label(self, text=tip)
        self.instr_label.grid(row=0, column=1, sticky=tk.N ,padx=10, pady=5)

        # Mk and show Items Labels and Entries
        self.sl, self.ul, self.pl = f'{self.s}:', f'{self.u}:', f'{self.p}:'    # l: per label
        self.rl, self.nl, self.npl = f'{self.r}:', f'{self.n}:', f'{self.np}:' 
        self.src_entry = self.__mk_item(self.sl, 2)
        self.usr_entry = self.__mk_item(self.ul, 3)
        self.pwd_entry = self.__mk_item(self.pl, 4)
        self.pw2_entry = self.__mk_item(self.pl, 5)
        self.url_entry = self.__mk_item(self.rl, 6)
        self.nts_entry = self.__mk_item(self.nl, 7)
        self.nxt_pwd_entry = self.__mk_item(self.npl, 8)
        self.nxt_pw2_entry = self.__mk_item(self.npl, 9)

        # Mk and show buttons w/their commands
        cmds = (self.add_pwd, self.get_pwd, self.get_tbl, self.get_usr, self.chg_pwd,
                self.chg_url, self.updt_nts, self.set_nxt_pwd, self.src_srch, self.del_src,
                self.table_by_src, self.tbl_icase, self.f_monti, self.clr_data, self.hlp)
        i = 0
        for r, c in itertools.product(range(1, 8), (2, 3)):
            if i == 13:
                break
            #ix = str(i + 1)
            ix = hex(i + 1)[-1].upper()
            self.__mk_btn(self.pmt.mthds[ix][0], cmds[i], r, c)
            i += 1
        self.__mk_btn('Clear Data', cmds[13], 7, 3)
        self.__mk_btn('Help', cmds[14], 8, 3)

    def __mk_item(self, txt, rw):
        c, px, py, w, shw = 0, 10, 5, 30, None
        if txt == self.nl or txt == self.rl:
            w = 120
        label = ttk.Label(text=txt)
        label.grid(row=rw, column=c, sticky=tk.W, padx=px, pady=py)
        if txt == self.pl or txt == self.npl:
            shw='*'
        entry = tk.Entry(width=w, show=shw)
        entry.grid(row=rw, column=c+1, sticky=tk.W, padx=px, pady=py)
        return entry
    
    def __mk_btn(self, txt, cmd, r, c):
        px, py, w = 10, 5, 30
        self.btn = ttk.Button(self, text=txt, command=cmd, width=18)
        self.btn.grid(row=r, column=c, sticky=tk.E, padx=px, pady=py)        

    def add_pwd(self):              # '1': ('Add Password', self.add_pwd)
        src = self.src_entry.get()
        usr = self.usr_entry.get()
        pwd = self.pwd_entry.get()
        pw2 = self.pw2_entry.get()
        url = self.url_entry.get()
        nts = self.nts_entry.get()
        nxt_pwd = self.nxt_pwd_entry.get()
        nxt_pw2 = self.nxt_pw2_entry.get()

        if src and usr and pwd:
            try:
                assert pwd == pw2
                if nxt_pwd != nxt_pw2:
                    raise UserWarning
                self.pmt.add_pwd(src, usr, pwd, url, nts, nxt_pwd)
                msb.showinfo("Success", "Password Successfully Added!")
                self.get_tbl()
            except AssertionError as e:
                msb.showwarning('Error', f"Passwords don't match {e}")
            except UserWarning as e:
                msb.showwarning('Error', f"Next Passwords (nxt_pwd) don't match {e}")
            except Exception as e:
                msb.showerror('CRITICAL ERROR', f'Can not add new Service \n {e}')
        else:
            msb.showwarning("Error", f'''
Please fill {self.sl}, {self.ul}, and {self.pl} fields.
{self.rl}, {self.nl} and {self.npl} are optional.''')

    def get_pwd(self):              # '2': ('Get Password', self.get_pwd)
        src = self.src_entry.get()
        try:
            pwd, nxt_pwd = self.pmt.get_pwd(src)
            msb.showinfo(self.pl, f'{pwd}\n{nxt_pwd}')
        except Exception as e:
            msb.showwarning('ERROR', f"Can't get password for Service '{src}'\n{e}")

    def get_tbl(self):                  # '3': ('Get Table', self.get_tbl
        try:
            ShowDF(self.pmt.get_tbl())
        except Exception as e:
            msb.showwarning('ERROR', f"Can't show the table\n{e}")
        
    def get_usr(self):                  # '4': ('Get User', self.get_usr)
        src = self.src_entry.get()
        try:
            msb.showinfo(self.ul, self.pmt.get_usr(src))
        except Exception as e:
            msb.showwarning('ERROR', f"Can't get user for Service '{src}'\n{e}")

    def chg_pwd(self):                  # '5': ('Change Password', self.chg_pwd)
        src = self.src_entry.get()
        n_pwd = self.pwd_entry.get()
        n_pw2 = self.pw2_entry.get()
        if src and n_pwd and n_pw2:
            try:
                assert n_pwd == n_pw2
                self.__chg_val(src, n_pwd, self.pmt.chg_pwd, 'Password Successfully Changed!')
            except AssertionError as e:
                msb.showwarning('Error', f"Passwords don't match {e}")
            except Exception as e:
                msb.showerror('CRITICAL ERROR', f'Can not Change Password of {self.s}: {src} \n {e}')
        else:
            msb.showwarning("Error", f"Please fill '{self.s}' and both '{self.p}' fields.")

    def __chg_val(self, src, val, mthd, msg=''):
        try:
            mthd(src, val)
            msb.showinfo("Success", msg)
            self.get_tbl()
        except Exception as e:
            msb.showinfo('Error', e)

    def chg_url(self):                  # '6': ('Change URL', self.chg_url)
        src = self.src_entry.get()
        n_url = self.url_entry.get()
        if src and n_url:
            self.__chg_val(src, n_url, self.pmt.chg_url, 'URL Successfully Changed!')
        else:
            msb.showwarning("Error", f"Please fill '{self.s}' and '{self.r}' fields.")

    def updt_nts(self):                 # '7': ('Update Notes', self.updt_nts)
        src = self.src_entry.get()
        n_nt = self.nts_entry.get()
        if src and n_nt:
            self.__chg_val(src, n_nt, self.pmt.updt_nts, 'Notes Successfully Updated!')
        else:
            msb.showwarning("Error", f"Please fill '{self.s}' and '{self.n}' fields.")

    def set_nxt_pwd(self):              # '8': ('Set Nxt Pwd', self.set_nxt_pwd)       
        src = self.src_entry.get()
        nxt_pwd = self.nxt_pwd_entry.get()
        nxt_pw2 = self.nxt_pw2_entry.get()
        if src and nxt_pwd:
            try:
                assert nxt_pwd == nxt_pw2
                self.__chg_val(src, nxt_pwd, self.pmt.set_nxt_pwd,
                               'Next Password Successfully Loaded!')
            except AssertionError as e:
                msb.showwarning('Error', f"Passwords don't match {e}")
            except Exception as e:
                msb.showerror('CRITICAL ERROR', f'Can not add Next Password \n {e}')
        else:
            msb.showwarning("Error", f"Please fill '{self.s}' and both '{self.np}' fields.")

    def src_srch(self):                 # '9': ('Service Search', self.src_srch)
        part_s = self.src_entry.get()
        if part_s:
            ShowDF(self.pmt.src_srch(part_s))
        else:
            ShowDF(self.pmt.get_empty_df())

    def del_src(self):                  # 'A': ('Delete Service', self.del_src)
        src = self.src_entry.get()
        try:
            self.pmt.del_src(src)
            msb.showinfo(f'Deleted {self.s}', f'{src} DELETED - No turning back')
            self.get_tbl()
        except Exception as e:
            msb.showwarning("Error", e)

    def table_by_src(self):             # 'B': ('Table by Service', self.tbl_b_src)
        ShowDF(self.pmt.tbl_b_src())

    def tbl_icase(self):                # 'C': ('Tbl Ignoring Case', self.tbl_icase)
        ShowDF(self.pmt.tbl_icase())

    def f_monti(self):                  # 'D': ('Full Monti', self.f_monti)
        pph3 = self.pph_entry.get()
        self.pph_entry.delete(0, tk.END)
        if pph3 == self.__pph:
            ShowDF(self.pmt.f_monti())
        else:
            ShowDF(self.pmt.get_empty_df())
            msb.showerror('Security Concern', 'Access Denied!')

    def clr_data(self):                  # cmd[13]
        ShowDF(self.pmt.get_empty_df())
        for e in (self.src_entry, self.usr_entry, self.pwd_entry, self.pw2_entry, self.url_entry,
                  self.nts_entry, self.nxt_pwd_entry, self.nxt_pw2_entry):
            e.delete(0, tk.END)         # Clean entries fields one by one

    def hlp(self):                      # cmd[14]
        msb.showinfo(f'{prg_tittle}  - Help', help)

    def __ctrl_m(self):                 # Secret
        pph4 = self.pph_entry.get()
        self.pph_entry.delete(0, tk.END)
        src = self.src_entry.get()
        if pph4 == self.__pph and src:
            ShowDF(self.pmt._PmTable__get_naked_row(src))

    def __ext_prg(self, msg):
        msb.showerror('CRITICAL ERROR', msg)
        self.destroy()


if __name__ == "__main__":
    app = PwdMgr()
    app.mainloop()