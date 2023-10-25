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

## Fundamentals - Pandas
All data is stored in a Pandas Dataframe consisting of five columns and one row for each service that is loaded. The columns and 
their order are Service, Username, Password, Notes, and date_time. Password data is stored encrypted, the rest in plain text. 
The dataframe is saved in an encrypted file.    
pmcore.py takes care of all the tasks of encryption, decryption, and administration of the dataframe. The UI components do not 
require the use of either encryption or decryption or Pandas at all.

## Example Data:
- Passphrase: ¡Argentina Campeón del Mundo 2022! - Tres campeonatos mundiales: 1978(Kempes), 1986('El Diego'), 2022(Messi).
- Dataframe (columnns= ['Service', 'Username', 'Password', 'Notes', 'date_time']).
	- row_0: first row, initial file data
	- row_1: realpython.com, jperez.pwdmgr@gmail.com, At_least_8_chars
	- row_2: reedit.com, jperez_pwdmgr, The_2nd_Pwd, dlthub.com


