## Routine of running AGDP APP

1. run **/server/database/init/db_insert.py** to initialize the database

issues:

$\bullet$ You may need to reconfigure database setting in **db_insert.py** according to your own mysql settings [line 161]

   user: 'root'	password: 'root' are used as default

$\bullet$ Make sure you've cd to **/server/database/init** before running **db_insert.py**, because relative paths are used.

2. run /server/app.py to start the server
3. type 'http://127.0.0.1:5000' in your browser(Google Chrome is recommended, port 5000 is used as default by Flask) to view AGDP platform

