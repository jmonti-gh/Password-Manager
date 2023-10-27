''' This is a Password Manager Core Module: pmcore.py

It stores all data (Service, Username, Password, Notes, and date_time) in a DF,
which is saved in an encrypted file.
In turn, passwords are saved with their own encryption.

I see practical import it under the pmc alias, ex.: import pmcore as pmc'''

__author__ = 'Jorge Monti'
__version__ = 1.5


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


class PmTable():
    ''' Core class: It hosts a dataframe that is written as an encrypted file
    each time it is modified'''
    def __init__(self, pph, cfn=cipe, kfn=kife):
        self.__pph = pph        
        self.cfn = cfn
        self.kfn = kfn
        self.s, self.u, self.p = 'Service', 'Username', 'Password'
        self.n, self.fh = 'Notes', 'date_time'
        self.cols = [self.s, self.u, self.p, self.n, self.fh]
        
        # if cipe do not exist initialize it, else read-it + check cols names
        if not self.chk_file(self.cfn):
            self.wrt_cipe(self.__init_df())
        self.__df = self.read_table()        # get df from cipe (implicit checking of pph)
        # Check cols read vs the defined ones
        if len([i for i, j in zip(self.cols, self.__df.columns) if i == j]) != len(self.cols):
            raise CsdColumnsNotMatch

        # if kife do not exist initialize it, else read it.
        if not self.chk_file(self.kfn):
            self.__wrt_kipe()
        self.__key = self.__read_key()         # get key from kife file

        self.mthds = {
            '1': ('Add Password', self.add_pwd), '2': ('Get Password', self.get_pwd),
            '3': ('Change Password', self.chg_pwd), '4': ('Update Notes', self.updt_nts),
            '5': ('Service Search', self.srv_srch), '6': ('Delete Service', self.del_srv),
            '7': ('Get Table', self.get_tbl), '8': ('Get User', self.get_usr),
            '9': ('Table by Service', self.tbl_b_srv), '10': ('Tbl Ignoring Case', self.tbl_icase),
            '11': ('Full Monti', self.f_monti)
            }
    
    def __shw_only(func):           # to hide some columns in table views (decorator)
        def inner(self, *args):
            return func(self, *args).drop([self.p, self.u], axis=1)
        return inner
        
    def chk_file(self, fnanme: str) -> bool:
        try: open(fnanme)
        except: return False
        else: return True

    def wrt_cipe(self, df: pd.DataFrame) -> None:
        ''' Write encrypted (cryptpandas) DF to file'''
        crp.to_encrypted(df, password=self.__pph, path=self.cfn)

    def __init_df(self) -> pd.DataFrame:
        row_0 = [['!csd', 'usr', 'pwd', 'First row', dtm.datetime.now()]]
        return pd.DataFrame(row_0, columns=self.cols)

    def read_table(self) -> pd.DataFrame:
        return crp.read_encrypted(path=self.cfn, password=self.__pph)
    
    def __wrt_kipe(self) -> None:
        '''Write Fernet.key to file'''
        k = Fernet.generate_key()
        with open(self.kfn, 'wb') as f:
            f.write(k)

    def __read_key(self) -> str.encode:
        with open(self.kfn, 'rb') as f:
            return f.read()
    
    ## '1': ('Add Password', 'add_pwd')
    def add_pwd(self, srv: str, usr: str, pwd: str, nts='') -> None:
        '''Add a complete row to the DF and write the asociate file'''
        self.__bk_srv(srv)  # Check if 'srv' is already loaded, if True mk a backup
        c_pwd = Crypts.crypt_str(self.__key, pwd)
        # Append new_values list to self.__df
        self.__df.loc[len(self.__df)] = [srv, usr, c_pwd, nts, dtm.datetime.now()]
        self.wrt_cipe(self.__df)

    def chk_srv(self, srv: str) -> bool:
        if not self.__df.loc[self.__df[self.s] == srv].empty:
            return True
        else: return False

    def __bk_srv(self, srv: str) -> None:
        '''If srv-row exists mk a backup-row adding date to srv_name'''
        if self.chk_srv(srv):
            s_row = self.__df.loc[self.__df[self.s] == srv]
            ix = s_row.index[0]
            self.__df.loc[ix, self.s] = f'''{srv}.>{s_row.loc[ix, self.fh].strftime('%b-%d')}'''
            self.wrt_cipe(self.__df)

    ## '2': ('Get Password', 'get_pwd')
    def get_pwd(self, srv: str) -> tuple():
        if self.chk_srv(srv):
            gp_row = self.__df.loc[self.__df[self.s] == srv]
            c_pwd = gp_row.loc[(ix := gp_row.index[0]), self.p]
            usr = gp_row.loc[ix, self.u]
            pwd = Crypts.dcyt_str(self.__key, c_pwd)
            return usr, pwd
        else:
            return None, None
    
    ## '3': ('Change Password', 'chg_pwd')
    def chg_pwd(self, srv: str, new_pwd: str) -> None:
        '''Change passwd in a row or return ServiceNotFoundError if srv do not exist'''
        if self.chk_srv(srv):
            cp_row = self.__df.loc[self.__df[self.s] == srv]
            c_pwd = Crypts.crypt_str(self.__key, new_pwd)       # Crypted password
            self.__df.loc[cp_row.index[0], self.p] = c_pwd
            self.wrt_cipe(self.__df)
        else:
            raise ServiceNotFoundError(val=srv)

    ## '4': ('Update Notes', 'updt_nts')    
    def updt_nts(self, srv: str, new_nt: str) -> None:
        '''Change passwd in a row or return ServiceNotFoundError if srv do not exist'''
        if self.chk_srv(srv):
            un_row = self.__df.loc[self.__df[self.s] == srv]
            self.__df.loc[un_row.index[0], self.n] = new_nt
            self.wrt_cipe(self.__df)
        else:
            raise ServiceNotFoundError(val=srv)

    ## '5': ('Service Search', 'srv_srch')
    @__shw_only
    def srv_srch(self, part_srv: str) -> pd.DataFrame:
        #return self.__df.loc[self.__df[self.s].str.contains(part_srv)]
        if part_srv.isupper():
            ps2 = part_srv.casefold()
        else:
            ps2 = part_srv.upper()
        return self.__df.loc[self.__df[self.s].str.contains(part_srv) |
                             self.__df[self.s].str.contains(ps2)]\
                                .sort_values(by=self.s, key=lambda x: x.str.casefold())

    ## '6': ('Delete Service', 'del_srv')
    def del_srv(self, srv: str) -> None:
        ''' Delete srv_row if srv existe, else return ServiceNotFoundError'''
        if self.chk_srv(srv):
            self.__df = self.__df[self.__df[self.s] != srv]
            self.wrt_cipe(self.__df)
        else:
            raise ServiceNotFoundError(val=srv)

    ## '7': ('Get Table', 'get_tbl')
    @__shw_only
    def get_tbl(self) -> pd.DataFrame:
        return self.__df
    
    ## '8': ('Get User', self.get_usr)
    def get_usr(self, srv: str) -> str or None:
        if self.chk_srv(srv):
            gu_row = self.__df.loc[self.__df[self.s] == srv]
            return gu_row.loc[gu_row.index[0], self.u]
        else:
            return None
    
    ##  '9': ('Table by Service', self.tbl_b_srv)
    @__shw_only
    def tbl_b_srv(self):
        return self.__df.sort_values(by=[self.s])

     ##  '10': ('Tbl Ignoring Case', self.tbl_icase)
    @__shw_only
    def tbl_icase(self):
        return self.__df.sort_values(by=[self.s],
                                     key=lambda x: x.str.casefold())

    ## '11': ('Full Monti', self.f_monti)
    def f_monti(self) -> pd.DataFrame:
        return self.__df

    def get_cols(self) -> list:
        return self.cols
    
    def get_empty_df(self) -> pd.DataFrame:
        return pd.DataFrame(columns=self.cols)
    

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
    passphrase = input('Passphrase: ')
    pmc1 = PmTable(passphrase)
    print(pmc1.f_monti())