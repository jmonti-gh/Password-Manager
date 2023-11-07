# Administrador y Almacen de contraseñas con Pandas (ver. 3.0)
Administra y almacena de forma encriptada contraseñas y datos de conexión para una ilimitada cantidad de servicios.
- Asimismo en este repo encontrarpa exemplos de conexión a Bases de Datos, logins a sitios web y a servidores ssh (y un 'lanzador de scripts', 
desde donde podrá ejecutar todas esas cnexiones)
- Todos estos exemplos utilizan el módulo 'pmcore', el corazón the este proyecto, que es el que permite acceder a las credenciales almacenadas.

## Proposito
Este proyecto nace de la necesidad de contar con un almacen seguro de credenciales del cual leer datos de usuario y contraseña principalmente 
para automatizar el logeo a diferentes servicios, sitos de internet, conexiones a bases de datos, etc.
Los ejemplos de conexión a este tipo de servicios que encuentra en este repo utilizan librerías como Selenium 4 (Web e Intranet), PyAutoGUI 
(local apps., Web, Intranet) y conectores a Bases de Datos.

## Archivos en este repositorio (en orden algabético)
- cipe.csd and nert: comentados más abajo.
- pmcore.py: módulo python escencial de este proyecto, en el próximo punto se detalla el mismo.
- pmgui: Win Shortcut(.lnk) for pmgui.pyw execution.
- pmgui.pyw: Tkinter Password Manager GUI.
- pmtui.py: Password Manager Text-based user interface (TUI).
- README.md: this file.
- scripts_launcher: Win Shortcut(.lnk) for scripts_launcher.pyw execution.
- scripts_launcher.pyw: Basic GUI to launch python scripts (and others executables...).
- website_login.py: selenium 4 websites login automation.

## pmcore.py
Como ya hemos señalado anteriormente este es el múdulo central de esta solución de almacenamiento y gestión de credenciales encriptadas.
Se encarga de llevar a cabo todas las tareas de bakend como encripción, gestión de los datos de la tabla, lectura y escritura de la tabla encriptada.
Todas las demás aplicaciones de este proyecto hacen uso de este módulo para leer las credenciales necesarias según el servicio o, en el caso particular
de las interfaces de usuario para la administración (pmtui.py y pmgui.pyw), manejar las altas, bajas y modificaciones de los datos de la tabla.
Asimismo contando con este módulo un programador de python o de cualquier lenguaje que pueda llamar módulos python puede escribir sus propias rutinas 
de administración o conexión con el servicio que necesite, sin necesidad de tener conocimientos de dataframes, pandas, escritura o lectura de archivos,
o mecanismos de encripción o desencripción, ya que de todo eso se encarga este módulo.
- Queda por experimentar la posibilidad de crear un ejecutable de este módulo (.exe en Win) y que sea llamdo desde un script en php por ej.

## Componentes
### Code
- pmcore.py, pmtui.py, pmgui.py, anteriormente descriptos.
### Archivos
1. cipe.csd: Tabla (pandas Dataframe) salvada de manera encriptada que contiene los datos de cada servicio.
2. nert: Archivo que contiene la key de ecripción de los campos Password y next_pwd de la tabla.
> La recomendación es almacenar el archivo 'nert' en el sitio más seguro posible para el usuario.
- Delete them and they will be created from scratch with a new passphrase when the PmTable() class is intantiated.
- cipe.csd and nert are files default names. Renames can be done using the cfn=, and kfn= parameters of the PmTable() class.
#### Formato de la tabla de datos
All data is stored in a Pandas Dataframe consisting of eigth columns and, for each service that is loaded, one new row. The columns and 
their order are:    
1. Service: name of the service. (Must be unique, not posible to load two of the same name) (str)
2. Username: username to login to the service (str)
3. Password: password to login to the service (encrypted)
4. URL_IPport: Web url or IP:port data necessary to locate the service (ex. https://www.reedit.com/, or 192.168.3.3:22)
5. Domain: Third field that define domain to connect (MS-AD Domain, or Cloud Tenant, or DB Instance, etc.)
5. dt_pwd: Datetime password was load or changed.
6. Notes: general notes, comments, etc.
7. next_pwd: potential password to change nex password change in the service.
8. dt_next_pwd: Datatime next_pwd was loaded or chenged (setted).         
The dataframe is saved in an encrypted file (default name: cipe.csd)    
pmcore.py takes care of all the tasks of encryption, decryption, and administration of the dataframe. The UI components do not 
require the use of either encryption nor decryption nor Pandas at all.

## pmcore.py classes (brief)
### class pmcore.PmTable(pph=None, cfn='cipe.csd', kfn='nert')
    ''' Core class: It hosts a dataframe that is written as an encrypted file
    each time it is modified'''
#### Parameters
- pph: passphrase. Must be passed.
- cfn: Cripted file name with path.
- kfn: Encryption Key file name whith path.
#### Attributes - Methods
        self.mthds = {
            '1': ('Add Service', self.addsrc), '2': ('Get Password', self.getpwd),
            '3': ('Get Table', self.gettbl), '4': ('Get User', self.getusr),
            '5': ('Change Password', self.chgpwd), '6': ('Change URL', self.chgurl),
            '7': ('Update Notes', self.updtnts), '8': ('Set Next Pwd', self.setnxtpwd),
            '9': ('Service Search', self.srcsrch), 'A': ('Delete Service', self.delsrc),
            'B': ('Table by Service', self.tblsrc), 'C': ('Tbl Ignoring Case', self.tblicase),
            'D': ('Full Monti', self.fmonti), 'E': ('Get URL', self.geturl),
            'F': ('Get Domain', self.getdom)
            }
		self.__df
### class ServiceNotFoundError(ValueError), and class CsdColumnsNotMatch(TypeError):
Own Exceptions definition.
### class Crypts():
    ''' Goup of functions that deal with encryption'''
	
## Pricipio de funcionamiento de pmcore - Pandas
Cuando la clase PmTable de pmcore es instanciada lee, si es que existen, o crea de cero, si es que no existen ,los archivos que 
por defualt hemos llamado cipe.csd y nert. Esto lo hará en el camino (path) que sea indicado por la aplicación que llama a la clase.
Los archivos cipe.csd y nert pueden almacenarse en distintos subdirectorios (diferentes paths para c/uno), por supuesto con diferentes
nombres a los propuestos por default. El único requisito es que la aplicación tenga acceso de escritura para cipe.csd y de lectura para
nert (una vez que este último haya sido creado por primera vez).



## Example Data:
- Passphrase: Simple 678!
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
