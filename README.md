# Password Manager with Pandas
To manage and store access credentials for countless services.

## Purpose
This project was born from the need to have a secure repository from which to read user and password data to automate the login to different services on the Web or intranet.

## Components
1. pmcore.py: Central python module in charge of carrying out all backend tasks.
2. pmterm.py: Text-mode user interface.
3. pmtk.py: GUI using tkinter.

## Fundamentals - Pandas
All data is stored in a Pandas Dataframe consisting of five columns and one row for each service that is loaded. The columns and their order are Service, Username, Password, Notes, and fecha_hora. Password data is stored encrypted, the rest in plain text. The dataframe is saved in an encrypted file.    
pmcore.py takes care of all the tasks of encryption, decryption, and administration of the dataframe. The UI components do not require the use of either encryption or decryption or Pandas at all.

