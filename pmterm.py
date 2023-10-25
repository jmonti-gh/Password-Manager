#!/usr/bin/env python

# pmterm.py

'''
tex-terminal front-end for a Password Manager Program
'''

####################################################
prg_tittle = ''' Password Manager -terminal- v1.5'''
####################################################
# author: Jorge Monti

import getpass as gp                # Built-in Lib
from tabulate import tabulate       # External Lib
import pmcore as pmc                # Own module


### Functions
def input_scrt(txt):
    while True:
        # scrt1 = gp.getpass(f'Input {txt}: ')
        # scrt2 = gp.getpass(f'Re-enter {txt}: ')
        scrt1 = input(f'Input {txt}: ')
        scrt2 = input(f'Re-enter {txt}: ')
        if scrt1 == scrt2:
            break
        else:
            print(f'{txt}s do not match!, try again...')
    return scrt1
    
def input_val(val):
    res = input(f'Input {val}: ')
    return res

def chg_val(srv, val, mthd, succ=''):
    try:
        mthd(srv, val)
        print(succ)
    except Exception as e:
        print(f'Error: {e}')

    
### main
print(f' ~~~~ {prg_tittle} ~~~~')
passphrase = input_scrt('Passphrase')
pmc1 = pmc.PmTable(passphrase)
s, u, p, n, dt = pmc1.get_cols()

# Menu
while True:
    print()
    for k, v in pmc1.mthds.items():
        print(f'{k}) {v[0]}')
    
    option = input('Select an option [0 to quit program]: ')

    
    if option == '1':                   # add_pwd
        srv = input_val(s)
        usr = input_val(u)
        pwd = input_scrt(p)
        nts = input_val(n)
        try:
            pmc1.add_pwd(srv, usr, pwd, nts)
            print('Password Successfully Added!')
        except Exception as e:
            print(f'Error! {e}')
    
    elif option == '2':                 # get_pwd
        srv = input_val(s)
        print(pmc1.get_pwd(srv)[1])

    elif option == '3':                 # chg_pwd
        srv = input_val(s)
        n_pwd = input_scrt(p)
        chg_val(srv, n_pwd, pmc1.chg_pwd, 'Password Successfully Changed!')

    elif option == '4':                 # updt_nts
        srv = input_val(s)
        n_nt = input_val(n)
        chg_val(srv, n_nt, pmc1.updt_nts, 'Notes Successfully Updated!')

    elif option == '5':                 # srv_srch
        part_s = input(f'Input the name of the service or part of the name: ')
        print(tabulate(pmc1.srv_srch(part_s), headers='keys', tablefmt='psql'))

    elif option == '6':                 # del_srv
        srv = input_val(s)
        if pmc1.chk_srv(srv):
            pmc1.del_srv(srv)
            print(f'{srv} DELETED - No turning back')
        else:
            print(f'Error: {s} "{srv}" do not exists!')

    elif option == '7':                 # get_tbl
        #print(pmc1.get_tbl())
        print(tabulate(pmc1.get_tbl(), headers='keys', tablefmt='psql'))
    
    elif option == '8':                 # get_usr
        srv = input_val(s)
        print(pmc1.get_usr(srv))

    elif option == '9':                 # get_t_by_srv
        #print(pmc1.tbl_b_srv())
        print(tabulate(pmc1.tbl_b_srv(), headers='keys', tablefmt='psql'))
    
    elif option == '10':                # '10': ('Tbl Ignoring Case', self.tbl_icase),
        #print(pmc1.tbl_icase())
        print(tabulate(pmc1.tbl_icase(), headers='keys', tablefmt='psql'))

    elif option == '11':                # '11': ('Full Monti', self.f_monti)
        pph3 = gp.getpass('Please enter Passphrase: ')   
        if pph3 == passphrase:
            print(pmc1.f_monti())
        else:
            print('Acces Denied!')

    elif option == '0':
        quit()

    else:
        print(f'Not a valid option: {option}: ')
    

