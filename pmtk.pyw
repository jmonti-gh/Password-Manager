# C:\Windows\pyw.exe

# pmtk.pyw

'''
tkinter GUI front-end for a Password Manager Program
'''

#######################################################
prg_tittle = ''' Password Manager -tkinter- v 1.5''' 
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


### Universal Vars
instructions = '''| Add Password |\t> Fill the fields to add a new Service.
| Service Search |\t> Enter part of the Service name (ignores case). 
| Full Monti |\t> Displays the entire Table.'''

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
        f.grid(row=7, columnspan=3, pady=10)
        pt = Table(f, dataframe=df, showstatusbar=True)
        pt.editable = False
        pt.show()


class PwdMgr(tk.Tk):
    ''' Full tkinter Password Manager App'''
    def __init__(self):
        super().__init__()
        self.title(prg_tittle)
        self.resizable(0, 0)
        self.grid_columnconfigure(1, minsize=100)
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
            self.pmc1 = pmc.PmTable(self.__pph)
        except Exception as e:
            self.__ext_prg(f'Critical Error getting Table: {e}')
        else:
            # get columns names as independent vars
            self.s, self.u, self.p, self.n, self.fh = self.pmc1.get_cols()
            self.pph2_entry.delete(0, tk.END)   
            self.pph_btn.destroy()              # Delete pph_btn 'OK' button
            self.pph_entry.delete(0, tk.END)    # Clean passphrase field
            self.pph2_entry.destroy()             
            self.label2.destroy()
            self.main_widgets()                 # Build whole window (wo/table yet)
        return True
    
    def main_widgets(self):
        # Show Instructions Label
        self.instr_label = ttk.Label(self, text=instructions)
        self.instr_label.grid(row=0, column=1, sticky=tk.N ,padx=10, pady=5)

        # Mk and show Items Labels and Entries
        self.sl, self.ul = f'{self.s}:', f'{self.u}:'   # l: per label
        self.pl, self.nl = f'{self.p}:', f'{self.n}:'
        self.srv_entry = self.__mk_item(self.sl, 2)
        self.usr_entry = self.__mk_item(self.ul, 3)
        self.pwd_entry = self.__mk_item(self.pl, 4)
        self.pw2_entry = self.__mk_item(self.pl, 5)
        self.nts_entry = self.__mk_item(self.nl, 6)

        # Mk and show 10 buttons w/their commands
        cmds = (self.add_pwd, self.get_pwd, self.chg_pwd, self.updt_nts,
                self.srv_srch, self.del_srv, self.get_tbl, self.get_usr,
                self.table_by_srv, self.tbl_icase, self.f_monti, self.clr_data)
        i = 0
        for r, c in itertools.product(range(1, 7), (2, 3)):
            if i == 11:
                break
            ix = str(i + 1)
            self.__mk_btn(self.pmc1.mthds[ix][0], cmds[i], r, c)
            i += 1
        self.__mk_btn('Clear Data', cmds[11], 6, 3)
        
    def __mk_item(self, txt, r):
        c, px, py, w, shw = 0, 10, 5, 30, None
        if txt == self.nl:
            w = 120
        label = ttk.Label(text=txt)
        label.grid(row=r, column=c, sticky=tk.W, padx=px, pady=py)
        if txt == self.pl:
            shw='*'
        entry = tk.Entry(width=w, show=shw)
        entry.grid(row=r, column=c+1, sticky=tk.W, padx=px, pady=py)
        return entry
    
    def __mk_btn(self, txt, cmd, r, c):
        px, py, w = 10, 5, 30
        self.btn = ttk.Button(self, text=txt, command=cmd, width=18)
        self.btn.grid(row=r, column=c, sticky=tk.E, padx=px, pady=py)        

    def add_pwd(self):          # 1: add_pwd
        srv = self.srv_entry.get()
        usr = self.usr_entry.get()
        pwd = self.pwd_entry.get()
        pw2 = self.pw2_entry.get()
        nts = self.nts_entry.get()
        if srv and usr and pwd:
            try:
                assert pwd == pw2
                self.pmc1.add_pwd(srv, usr, pwd, nts)
                msb.showinfo("Success", "Password Successfully Added!")
            except AssertionError as e:
                msb.showwarning('Error', f"Passwords don't match {e}")
            except Exception as e:
                msb.showerror('CRITICAL ERROR', f'Can not add new Service \n {e}')
        else:
            msb.showwarning("Error",
                            f'''Please fill {self.sl}, {self.ul}, and {self.pl} fields
                            {self.nl}' is optional.''')

    def get_pwd(self):              # 2: get_pwd
        srv = self.srv_entry.get()
        try:
            msb.showinfo(self.pl, self.pmc1.get_pwd(srv)[1])
        except Exception as e:
            msb.showwarning('ERROR', f"Can't get password of Service '{srv}'\n{e}")

    def chg_pwd(self):                # 3: chg_pwd
        srv = self.srv_entry.get()
        n_pwd = self.pwd_entry.get()
        if srv and n_pwd:
            self.__chg_val(srv, n_pwd, self.pmc1.chg_pwd, 'Password Successfully Changed!')
        else:
            msb.showwarning("Error", f"Please fill '{self.s}' and '{self.p}' fields.")

    def updt_nts(self):             # 4: updt_nts
        srv = self.srv_entry.get()
        n_nt = self.nts_entry.get()
        if srv and n_nt:
            self.__chg_val(srv, n_nt, self.pmc1.updt_nts, 'Notes Successfully Updated!')
        else:
            msb.showwarning("Error", f"Please fill '{self.s}' and '{self.n}' fields.")

    def __chg_val(self, srv, val, mthd, succ=''):
        try:
            mthd(srv, val)
            msb.showinfo("Success", succ)
        except Exception as e:
            msb.showinfo('Error', e)

    def srv_srch(self):                     # 5: srv_srch
        part_s = self.srv_entry.get()
        if part_s:
            ShowDF(self.pmc1.srv_srch(part_s))
        else:
            ShowDF(self.pmc1.get_empty_df())

    def del_srv(self):                      # 6: del_srv
        srv = self.srv_entry.get()
        try:
            self.pmc1.del_srv(srv)
            msb.showinfo(f'Deleted {self.s}', f'{srv} DELETED - No turning back')
        except Exception as e:
            msb.showwarning("Error", e)

    def get_tbl(self):                      # 7: get_tbl
        ShowDF(self.pmc1.get_tbl())

    def get_usr(self):                      # 8: get_usr
        srv = self.srv_entry.get()
        msb.showinfo(self.ul, self.pmc1.get_usr(srv))

    def table_by_srv(self):                 # 9: get_t_by_srv
        ShowDF(self.pmc1.tbl_b_srv())

    def tbl_icase(self):                    # 10: tbl_icase
        ShowDF(self.pmc1.tbl_icase())

    def f_monti(self):                      # 11: f_monti
        pph3 = self.pph_entry.get()
        self.pph_entry.delete(0, tk.END)
        if pph3 == self.__pph:
            ShowDF(self.pmc1.f_monti())
        else:
            ShowDF(self.pmc1.get_empty_df())
            msb.showerror('Security Concern', 'Access Denied!')

    def clr_data(self):                     # 12:
        ShowDF(self.pmc1.get_empty_df())
        for e in (self.srv_entry, self.usr_entry, self.pwd_entry, self.pw2_entry,
                  self.nts_entry):
            e.delete(0, tk.END)         # Clean entries fields one by one

    def __ext_prg(self, msg):
        msb.showerror('CRITICAL ERROR', msg)
        self.destroy()


if __name__ == "__main__":
    app = PwdMgr()
    app.mainloop()