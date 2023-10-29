# Password Manager with Pandas
To manage and store access credentials for countless services.

## Purpose
This project was born from the need to have a secure repository from which to read user and password data to automate the login to 
different services on the Web or intranet.

## Components
### Code
1. pmcore.py: Central python module in charge of carrying out all backend tasks.
2. pmterm.py: Text-mode user interface.
3. pmtk.py: GUI using tkinter.
### Files
1. cipe.csd: Dataframe saved as an encrypted file.
2. nert: Key file.
- Delete them and they will be created from scratch with a new passphrase when the PmTable() class is intantiated.
- cipe.csd and nert are files default names. Renames can be done using the cfn=, and kfn= parameters of the PmTable() class.

## pmcore.py classes
### class pmcore.PmTable(pph=None, cfn='cipe.csd', kfn='nert')
#### Parameters - Attributes - Methods
        self.mthds = {
            '1': ('Add Password', self.add_pwd), '2': ('Get Password', self.get_pwd),
            '3': ('Get Table', self.get_tbl), '4': ('Get User', self.get_usr),
            '5': ('Change Password', self.chg_pwd), '6': ('Change URL', self.chg_url),
            '7': ('Update Notes', self.updt_nts), '8': ('Set Next Pwd', self.set_nxt_pwd),
            '9': ('Service Search', self.src_srch), 'A': ('Delete Service', self.del_src),
            'B': ('Table by Service', self.tbl_b_src), 'C': ('Tbl Ignoring Case', self.tbl_icase),
            'D': ('Full Monti', self.f_monti)
            }
		self.__df

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
- Passphrase: ¡Argentina Campeón del Mundo 2022! - Tres campeonatos mundiales: 1978(Kempes), 1986('El Diego'), 2022(Messi).
- Dataframe rows
	- row_0: first row, initial file data		# row_0 is created at the same moment of table creation.
	- row_1: realpython.com, jperez.pwdmgr@gmail.com, At_least_8_chars
	- row_2: reedit.com, jperez_pwdmgr, The_2nd_Pwd, dlthub.com


