#!/usr/bin/env python

# pmterm_3_0.py

'''
tex-terminal front-end for Password Manager Program
'''

#####################################################
prg_tittle = ''' Password Manager -terminal- v 3.0'''
#####################################################
# author: Jorge Monti


# Built-in Libs
import getpass as gp
import logging
import sys

# Own module
import pmcore as pmc


### Program Variables
path = ''
cipe = path + "cipe.csd"
kipe = path + 'nert'


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

pmt = pmc.PmTable(passphrase, cipe, kipe)
s, u, p, r, d, dt, n, np, nd = pmt.getcols()

# Menu
while True:
    print()
    c = 1
    for k, v in pmt.mthds.items():
        print(f'{k:}) {v[0]:<20}', end='')
        if not c % 4: print()
        c += 1
    option = input('\n--> Select an option [0 to quit program]: ').upper()

    if option == '1':                   # '1': ('Add Password', self.addsrc)
        src = input_val(s)
        usr = input_val(u)
        pwd = input_scrt(p)
        url = input_val(r)
        dom = input_val(d)
        nts = input_val(n)
        nxt_pwd = input_scrt(np)

        if src and usr and pwd:
            try:
                pmt.addsrc(src, usr, pwd, url, dom, nts, nxt_pwd)
                print('Password Successfully Added!')
            except Exception as e:
                log.error(e)
        else:
            log.warning(f'''Please fill {s}, {u}, and {p} fields. {r}, {d}, {n} and {np} are optional.''')
    
    elif option == '2':                 # '2': ('Get Password', self.getpwd)
        src = input_val(s)
        try:
            pwd, nxt_pwd = pmt.getpwd(src)
            print(pwd, '\n', nxt_pwd)
        except pmc.ServiceNotFoundError as e:
            log.error(e)

    elif option == '3':                 # '3': ('Get Table', self.gettbl)
        print(pmt.gettbl())

    elif option == '4':                 # '4': ('Get User', self.get_usr)
        src = input_val(s)
        print(pmt.getusr(src))

    elif option == '5':                 # '5': ('Change Password', self.chg_pwd)
        src = input_val(s)
        n_pwd = input_scrt(p)
        chg_val(src, n_pwd, pmt.chgpwd, 'Password Successfully Changed!')

    elif option == '6':                 # '6': ('Change URL', self.chg_url),
        src = input_val(s)
        n_url = input_scrt(r)
        chg_val(src, n_url, pmt.chgurl, 'URL Successfully Changed!')

    elif option == '7':                 # '7': ('Update Notes', self.updt_nts)
        src = input_val(s)
        n_nt = input_val(n)
        chg_val(src, n_nt, pmt.updtnts, 'Notes Successfully Updated!')

    elif option == '8':                 # '8': ('Set Next Pwd', self.set_nxt_pwd)
        src = input_val(s)
        nxt_pwd = input_scrt(np)
        chg_val(src, nxt_pwd, pmt.setnxtpwd, 'Next Password Successfully Load!')

    elif option == '9':                 #  '9': ('Service Search', self.src_srch)
        part_s = input(f'Input the name of the service or part of the name: ')
        print(pmt.srcsrch(part_s))

    elif option == 'A':                 # 'A': ('Delete Service', self.del_src)
        src = input_val(s)
        if pmt.chksrc(src):
            pmt.delsrc(src)
            print(f'{src} DELETED - No turning back')
        else:
            log.warning(f'Error: {s} "{src}" do not exists!')

    elif option == 'B':                 # 'B': ('Table by Service', self.tbl_b_src)
        print(pmt.tblsrc())

    elif option == 'C':                 # 'C': ('Tbl Ignoring Case', self.tbl_icase)
        print(pmt.tblicase())   

    elif option == 'D':                # 'D': ('Full Monti', self.f_monti)
        pph3 = gp.getpass('Please enter Passphrase: ')   
        if pph3 == passphrase:
            print(pmt.fmonti())
        else:
            log.error('Access Denied!')

    elif option == 'E':                 # 'E': ('Get URL', self.get_url)
        src = input_val(s)
        print(pmt.geturl(src))

    elif option == 'F':                 # 'F': ('Get Domain', self.getdom)
        src = input_val(s)
        print(pmt.getdom(src))

    elif option == 'SECRET':             # Show HIDES in all row
        src = input_val(s)
        print(pmt._PmTable__get_naked_row(src))

    elif option == '0':
        sys.exit(f'{prg_tittle}, closed by user - Option: {option}')

    else:
        log.warning(f'Not a valid option: {option}: ')
    

