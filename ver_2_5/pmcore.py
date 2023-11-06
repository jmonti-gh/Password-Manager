''' This is a Password Manager Core Module: pmcore.py

It stores all data (Service, Username, Password, URL, dt_pwd, Notes, next_pwd, and dt_next_pwd)
in a DF, which is saved in an encrypted file (dt: datetime).
In turn, passwords are saved with their own encryption.

I see practical import it under the pmc alias, ex.: import pmcore as pmc'''

__author__ = 'Jorge Monti'
__version__ = 2.5


# Built-in Libraries
import datetime as dtm

# 3er Party Libs
import pandas as pd
import cryptpandas as crp
from cryptography.fernet import Fernet


cipe = 'cipe.csd'       # Crypted Dataframe filename
kife = 'nert'           # key filename


class ServiceNotFoundError(ValueError):
    ''' Raise when service do no exists in table DF'''
    def __init__(self, msg='Service do not exist in table', val=None, *args):
        self.msg = msg
        self.val = val
    def __str__(self) -> str:
        return f'{self.msg}: {self.val}'

class CsdColumnsNotMatch(TypeError):
    ''' Raise when columns of read csv are different from the defined en PmTable class'''
    def __str__(self) -> str:
        return 'The columns of the read file do not match those defined in this library'


class PmTable():
    ''' Core class: It hosts a dataframe that is written as an encrypted file
    each time it is modified'''
    def __init__(self, pph, cfn=cipe, kfn=kife):
        self.kfn = kfn
        self.__pph = pph        
        self.cfn = cfn
        self.s, self.u, self.p, self.r = 'Service', 'Username', 'Password', 'URL'
        self.d, self.n, self.np, self.nd = 'dt_pwd', 'Notes', 'next_pwd', 'dt_next_pwd'
        self.cols = [self.s, self.u, self.p, self.r, self.d, self.n, self.np, self.nd]
        self.M = dtm.datetime(1970,1,2)     # for empty dt_next_pwd entries (near ux_epoch == 0)
        self.mthds = {
            '1': ('Add Password', self.add_pwd), '2': ('Get Password', self.get_pwd),
            '3': ('Get Table', self.get_tbl), '4': ('Get User', self.get_usr),
            '5': ('Change Password', self.chg_pwd), '6': ('Change URL', self.chg_url),
            '7': ('Update Notes', self.updt_nts), '8': ('Set Next Pwd', self.set_nxt_pwd),
            '9': ('Service Search', self.src_srch), 'A': ('Delete Service', self.del_src),
            'B': ('Table by Service', self.tbl_b_src), 'C': ('Tbl Ignoring Case', self.tbl_icase),
            'D': ('Full Monti', self.f_monti), 'E': ('Get URL', self.get_url)
            }

        # if cipe do not exist initialize it, else read-it plus check cols names
        if not self.chk_file(self.cfn):
            self.wrt_cipe(self.__init_df())
        self.__df = self.read_table()       # get df from cipe (implicit checking of pph)
        # Check cols read vs the defined ones (comparing two lists)
        if len([i for i, j in zip(self.cols, self.__df.columns) if i == j]) != len(self.cols):
            raise CsdColumnsNotMatch
        
        # if kipe (key) don't exist create it (write it), else read-it
        if not self.chk_file(self.kfn):
            self.__wrt_kipe()
        self.__key = self.__read_key()      # get key from kife file
    
    def __shw_only(func):                   # to hide some columns in table views (decorator)
        def inner(self, *args):
            return func(self, *args).drop([self.p, self.u, self.np], axis=1)
        return inner
        
    def chk_file(self, fnanme: str) -> bool:
        try: open(fnanme)
        except: return False
        else: return True

    def wrt_cipe(self, df: pd.DataFrame) -> None:
        ''' Write encrypted (cryptpandas) DF to file'''
        crp.to_encrypted(df, password=self.__pph, path=self.cfn)

    def __init_df(self) -> pd.DataFrame:
        row_0 = [['!csd', 'usr', 'pwd', 'https://...', dtm.datetime.now(),
                  'row_0 (dt: date_time)', 'nxt_pwd', self.M]]
        return pd.DataFrame(row_0, columns=self.cols)
        # pwd and nxt_pwd aren't crypted (to see in future versions)

    def read_table(self) -> pd.DataFrame:
        return crp.read_encrypted(path=self.cfn, password=self.__pph)
    
    def __wrt_kipe(self) -> None:
        '''Write Fernet.key to file'''
        k = Crypts.gen_key()
        with open(self.kfn, 'wb') as f:
            f.write(k)

    def __read_key(self) -> bytes:
        with open(self.kfn, 'rb') as f:
            return f.read()

    def chk_src(self, src: str) -> bool:
        '''Check Check if a given service is already loaded in the DF'''
        if not self.__df.loc[self.__df[self.s] == src].empty:
            return True
        else: return False      
    
    ## '1': ('Add Password', 'add_pwd')
    def add_pwd(self, src: str, usr: str, pwd: str, url='', nts='', nxt_pwd='') -> None:
        '''Add a complete row to the DF and write the associate file'''
        self.__bk_src(src)                          # Check if 'src' is already loaded, if True mk a backup
        c_pwd = Crypts.crypt_str(self.__key, pwd)   # Encrypt pwd string
        now = dt_np = dtm.datetime.now()
        if not nxt_pwd:                     # if there's no next-password value:
            dt_np, c_nxt_pwd = self.M, ''   # date_time for nxt_pwd is 1980.1.1 and crypted next_pwd is empty
        else:
            c_nxt_pwd = Crypts.crypt_str(self.__key, nxt_pwd)

        # Append new-values-list to self.__df
        self.__df.loc[len(self.__df)] = [src, usr, c_pwd, url, now, nts, c_nxt_pwd, dt_np]
        self.wrt_cipe(self.__df)

    def __bk_src(self, src: str) -> None:
        '''If src-row exists mk a backup-row adding date to src_name'''
        if self.chk_src(src):
            s_row = self.__df.loc[self.__df[self.s] == src]
            ix = s_row.index[0]
            self.__df.loc[ix, self.s] = f'''{src}.>{s_row.loc[ix, self.d].strftime('%b-%d')}'''
            self.wrt_cipe(self.__df)

    ## '2': ('Get Password', 'get_pwd')
    def get_pwd(self, src: str) -> str:
        row = self.__get_naked_row(src)
        return row.loc[(row.index[0]), [self.p, self.np]]
        
    ## '3': ('Get Table', self.get_tbl)
    @__shw_only
    def get_tbl(self) -> pd.DataFrame:
        return self.__df

    ## '4': ('Get User', self.get_usr)
    def get_usr(self, src: str) -> str:
        row = self.__get_naked_row(src)
        return row.loc[(row.index[0]), self.u]

    ## '5': ('Change Password', self.chg_pwd),
    def chg_pwd(self, src: str, new_pwd: str) -> None or ServiceNotFoundError:
        '''Change Password in a src-row or return ServiceNotFoundError if src do not exist'''
        if self.chk_src(src):
            cp_row = self.__df.loc[self.__df[self.s] == src]
            c_pwd = Crypts.crypt_str(self.__key, new_pwd)       # Crypted password
            self.__df.loc[cp_row.index[0], self.p] = c_pwd
            self.__df.loc[cp_row.index[0], self.d] = dtm.datetime.now()
            self.wrt_cipe(self.__df)
        else:
            raise ServiceNotFoundError(val=src)

    ## '6': ('Change URL', self.chg_url),
    def chg_url(self, src: str, new_url: str) -> None or ServiceNotFoundError:
        '''Change url in a src-row or return ServiceNotFoundError if src do not exist'''
        if self.chk_src(src):
            cu_row = self.__df.loc[self.__df[self.s] == src]
            self.__df.loc[cu_row.index[0], self.r] = new_url
            self.wrt_cipe(self.__df)
        else:
            raise ServiceNotFoundError(val=src)

    ## '7': ('Update Notes', self.updt_nts) 
    def updt_nts(self, src: str, new_nt: str) -> None:
        '''Updates Notes in a src-row or return ServiceNotFoundError if src do not exist'''
        if self.chk_src(src):
            un_row = self.__df.loc[self.__df[self.s] == src]
            self.__df.loc[un_row.index[0], self.n] = new_nt
            self.wrt_cipe(self.__df)
        else:
            raise ServiceNotFoundError(val=src)

    ## '8': ('Set Next Pwd', self.set_next_pwd)
    def set_nxt_pwd(self, src: str, nxt_pwd):
        if self.chk_src(src):
            cp_row = self.__df.loc[self.__df[self.s] == src]
            c_nxt_pwd = Crypts.crypt_str(self.__key, nxt_pwd)       # Crypted next_password
            self.__df.loc[cp_row.index[0], self.np] = c_nxt_pwd
            self.__df.loc[cp_row.index[0], self.nd] = dtm.datetime.now()
            self.wrt_cipe(self.__df)
        else:
            raise ServiceNotFoundError(val=src)
        
    ## '9': ('Service Search', self.src_srch)
    @__shw_only
    def src_srch(self, part_src: str) -> pd.DataFrame:
        '''Search for services that contain the text ignoring case'''
        return self.__df.loc[self.__df[self.s].str.contains(part_src, case=False)]\
                                .sort_values(by=self.s, key=lambda x: x.str.casefold())

    ##'A': ('Delete Service', self.del_src)
    def del_src(self, src: str) -> None:
        ''' Delete src_row if src existe, else return ServiceNotFoundError'''
        if self.chk_src(src):
            self.__df = self.__df[self.__df[self.s] != src].reset_index(drop=True)
            self.wrt_cipe(self.__df)
        else:
            raise ServiceNotFoundError(val=src)

    ## 'B': ('Table by Service', self.tbl_b_src)
    @__shw_only
    def tbl_b_src(self) -> pd.DataFrame:
        ''' Sort 'Service' values, Capitals first'''
        return self.__df.sort_values(by=[self.s])
    
    ## 'C': ('Tbl Ignoring Case', self.tbl_icase)
    @__shw_only
    def tbl_icase(self) -> pd.DataFrame:
        '''Sort 'Service' values ignoring case'''
        return self.__df.sort_values(by=[self.s],
                                     key=lambda x: x.str.casefold())

    ## 'D': ('Full Monti', self.f_monti)
    def f_monti(self) -> pd.DataFrame:
        return self.__df
    
    ## 'E': ('Get URL', self.get_url)
    def get_url(self, src: str) -> str:
        row = self.__get_naked_row(src)
        return row.loc[(row.index[0]), self.r]

    def get_cols(self) -> list:
        return self.cols
    
    def get_empty_df(self) -> pd.DataFrame:
        return pd.DataFrame(columns=self.cols)
        
    def __get_naked_row(self, src: str) -> pd.DataFrame or ServiceNotFoundError:
        if self.chk_src(src):
            row = self.__df.loc[self.__df[self.s] == src]
            row.loc[ix, self.p] = Crypts.dcyt_str(self.__key, row.loc[(ix := row.index[0]), self.p])
            if row.loc[ix, self.np]:
                row.loc[ix, self.np] = Crypts.dcyt_str(self.__key, row.loc[ix, self.np])
            return row
        else:
            raise ServiceNotFoundError(val=src)
    
    
class Crypts():
    ''' Goup of functions that deal with encryption'''
    @staticmethod
    def gen_key():
        return Fernet.generate_key()

    @staticmethod
    def crypt_str(k, plain_str):
        f = Fernet(k)
        return f.encrypt(plain_str.encode()).decode()

    @staticmethod
    def dcyt_str(k, crypted_str):
        f = Fernet(k)
        return f.decrypt(crypted_str.encode()).decode()  
    

if __name__ == '__main__':
    # import os
    # os.system('python pmterm.py')

    o = PmTable("1978, 1986, and 2022 FIFA Champ!")
    #print(o.__dict__)





