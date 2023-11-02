#!/usr/bin/env python

# pmterm.py

'''
tex-terminal front-end for Password Manager Program.
'''

#####################################################
prg_tittle = ''' Password Manager -terminal- v 2.2'''
#####################################################
# author: Jorge Monti


# Built-in Libs
import getpass as gp
import logging
import sys

# Third-party Lib
from tabulate import tabulate  

# Own module
import pmcore as pmc


### Functions
def input_scrt(txt):
    while True:
        scrt1 = gp.getpass(f'Input {txt}: ')
        scrt2 = gp.getpass(f'Re-enter {txt}: ')
        if scrt1 == scrt2:
            break
        else:
            log.warning(f'{txt}s do not match!, try again...')
    return scrt1
    
def input_val(val):
    res = input(f'Input {val}: ')
    return res

def chg_val(src, val, mthd, succ=''):
    try:
        mthd(src, val)
        print(succ)
    except Exception as e:
        log.error(e)

    
### main
print(f' ~~~~ {prg_tittle} ~~~~')

# Config logging for warning and error messages
logging.basicConfig(format="[%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# If not passed as cli arg[1], ask user the passphrase, to get the password table and PmTable attributes.
try:
    passphrase = sys.argv[1]
except IndexError:
    passphrase = input_scrt('Passphrase')
except Exception as e:
    sys.exit(f'CRITICAL ERROR: {e}')

pmt = pmc.PmTable(passphrase)
s, u, p, r, d, n, np, nd = pmt.get_cols()

# Menu
while True:
    print()
    c = 1
    for k, v in pmt.mthds.items():
        print(f'{k:}) {v[0]:<20}', end='')
        if not c % 4: print()
        c += 1
    option = input('\n--> Select an option [0 to quit program]: ').upper()

    if option == '1':                   # '1': ('Add Password', self.add_pwd)
        src = input_val(s)
        usr = input_val(u)
        pwd = input_scrt(p)
        url = input_val(r)
        nts = input_val(n)
        nxt_pwd = input_scrt(np)

        if src and usr and pwd:
            try:
                pmt.add_pwd(src, usr, pwd, url, nts, nxt_pwd)
                print('Password Successfully Added!')
            except Exception as e:
                log.error(e)
        else:
            log.warning(f'''Please fill {s}, {u}, and {p} fields. {r}, {n} and {np} are optional.''')
    
    elif option == '2':                 # '2': ('Get Password', self.get_pwd)
        src = input_val(s)
        try:
            pwd, nxt_pwd = pmt.get_pwd(src)
            print(pwd, '\n', nxt_pwd)
        except pmc.ServiceNotFoundError as e:
            log.error(e)

    elif option == '3':                 # '3': ('Get Table', self.get_tbl)
        print(tabulate(pmt.get_tbl(), headers='keys', tablefmt='psql'))

    elif option == '4':                 # '4': ('Get User', self.get_usr)
        src = input_val(s)
        print(pmt.get_usr(src))

    elif option == '5':                 # '5': ('Change Password', self.chg_pwd)
        src = input_val(s)
        n_pwd = input_scrt(p)
        chg_val(src, n_pwd, pmt.chg_pwd, 'Password Successfully Changed!')

    elif option == '6':                 # '6': ('Change URL', self.chg_url),
        src = input_val(s)
        n_url = input_scrt(r)
        chg_val(src, n_url, pmt.chg_url, 'URL Successfully Changed!')

    elif option == '7':                 # '7': ('Update Notes', self.updt_nts)
        src = input_val(s)
        n_nt = input_val(n)
        chg_val(src, n_nt, pmt.updt_nts, 'Notes Successfully Updated!')

    elif option == '8':                 # '8': ('Set Next Pwd', self.set_nxt_pwd)
        src = input_val(s)
        nxt_pwd = input_scrt(np)
        chg_val(src, nxt_pwd, pmt.set_nxt_pwd, 'Next Password Successfully Load!')

    elif option == '9':                 #  '9': ('Service Search', self.src_srch)
        part_s = input(f'Input the name of the service or part of the name: ')
        print(tabulate(pmt.src_srch(part_s), headers='keys', tablefmt='psql'))

    elif option == 'A':                 # 'A': ('Delete Service', self.del_src)
        src = input_val(s)
        if pmt.chk_src(src):
            pmt.del_src(src)
            print(f'{src} DELETED - No turning back')
        else:
            log.warning(f'Error: {s} "{src}" do not exists!')

    elif option == 'B':                 # 'B': ('Table by Service', self.tbl_b_src)
        print(tabulate(pmt.tbl_b_src(), headers='keys', tablefmt='psql'))

    elif option == 'C':                 # 'C': ('Tbl Ignoring Case', self.tbl_icase)
        print(tabulate(pmt.tbl_icase(), headers='keys', tablefmt='psql'))   

    elif option == 'D':                # 'D': ('Full Monti', self.f_monti)
        pph3 = gp.getpass('Please enter Passphrase: ')   
        if pph3 == passphrase:
            print(pmt.f_monti())
        else:
            log.error('Access Denied!')

    elif option == 'E':                 # 'E': ('Get URL', self.get_url)
        src = input_val(s)
        print(pmt.get_url(src))

    elif option == 'SECRET':             # Show HIDES in all row
        src = input_val(s)
        print(tabulate(pmt._PmTable__get_naked_row(src), headers='keys'))

    elif option == '0':
        sys.exit(f'{prg_tittle}, closed by user - Option: {option}')

    else:
        log.warning(f'Not a valid option: {option}: ')
    

