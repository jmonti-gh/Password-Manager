# Password Manager with Pandas (ver. 2.5)
To manage and store access credentials for countless services.

## Purpose
This project was born from the need to have a secure repository from which to read user and password data to automate login to
different sites or services on the Web, or on the Intranet, or connections to Databases, or local applications that need
authenticatoin.    
Libraries such as selenium 4 (Web and Intranet), PyAutoGUI (Web, Intranet, local apps.), and DBs Connectors will be used to 
automate these logins.

## Files in this Repo (alphabetical order)
- cipe.csd and nert, commented above
- pmcore.py: Central python module in charge of carrying out all backend tasks.
- pmgui: Win Shortcut(.lnk) for pmgui.pyw execution.
- pmgui.pyw: Tkinter Password Manager GUI.
- pmtui.py: Password Manager Text-based user interface (TUI).
- README.md: this file.
- scripts_launcher: Win Shortcut(.lnk) for scripts_launcher.pyw execution.
- scripts_launcher.pyw: Basic GUI to launch python scripts (and others executables...).
- website_login.py: selenium 4 websites login automation.

## Password Manager Components
### Code
- pmcore.py, pmterm.py, pmtk.py, early described.
### Files
1. cipe.csd: Dataframe saved as an encrypted file.
2. nert: Key file.
- Delete them and they will be created from scratch with a new passphrase when the PmTable() class is intantiated.
- cipe.csd and nert are files default names. Renames can be done using the cfn=, and kfn= parameters of the PmTable() class.

## pmcore.py classes (brief)
### class pmcore.PmTable(pph=None, cfn='cipe.csd', kfn='nert')
    ''' Core class: It hosts a dataframe that is written as an encrypted file
    each time it is modified'''
#### Parameters
- pph: passphrase. Must be passed.
- cfn: Cripted file name.
- kfn: Encryption Key file name.
#### Attributes - Methods
        self.mthds = {
            '1': ('Add Password', self.add_pwd), '2': ('Get Password', self.get_pwd),
            '3': ('Get Table', self.get_tbl), '4': ('Get User', self.get_usr),
            '5': ('Change Password', self.chg_pwd), '6': ('Change URL', self.chg_url),
            '7': ('Update Notes', self.updt_nts), '8': ('Set Next Pwd', self.set_nxt_pwd),
            '9': ('Service Search', self.src_srch), 'A': ('Delete Service', self.del_src),
            'B': ('Table by Service', self.tbl_b_src), 'C': ('Tbl Ignoring Case', self.tbl_icase),
            'D': ('Full Monti', self.f_monti), 'E': ('Get URL', self.get_url)
            }
		self.__df
### class ServiceNotFoundError(ValueError), and class CsdColumnsNotMatch(TypeError):
Own Exceptions definition.
### class Crypts():
    ''' Goup of functions that deal with encryption'''

## Fundamentals - Pandas
All data is stored in a Pandas Dataframe consisting of eigth columns and, for each service that is loaded, one new row. The columns and 
their order are:    
1. Service: name of the service. (Must be unique, not posible to load two of the same name) (str)
2. Username: username to login to the service (str)
3. Password: password to login to the service (encrypted)
4. URL: (could be app launcher)
5. dt_pwd: Datetime password was load or changed.
6. Notes: general notes, comments, etc.
7. next_pwd: potential password to change nex password change in the service.
8. dt_next_pwd: Datatime next_pwd was loaded or chenged (setted).     
  
The dataframe is saved in an encrypted file (default name: cipe.csd)    
pmcore.py takes care of all the tasks of encryption, decryption, and administration of the dataframe. The UI components do not 
require the use of either encryption nor decryption nor Pandas at all.

## Example Data:
- Passphrase: 1978, 1986, and 2022 FIFA Champ!
- Dataframe rows
	- row_0: first row, initial file data		# row_0 is created at the same moment of table and crypto_key creation.
	- some_row: realpython.com, jperez.pwdmgr@gmail.com, At_least_8_chars, https://realpython.com/
	- some_row: reedit.com, jperez_pwdmgr, The_2nd_Pwd, https://www.reddit.com/, dlthub.com
	- some_row: etc... (the order don't care)

## Requeriments (It was only probe in Win10)
- Install python (python.org) - used in python 3.11
- pip install pandas, tabulate, selenium, pyautogui, pandastable

## Concept review
### python
#### Walrus operator
### Pandas
#### Different ways to concat (append) data to a DF
#### Sorting a DF
### Tkinter
